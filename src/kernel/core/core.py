from ..session.session_manager import SessionManager
from ..tools.tool_caller import tool_caller
from .components import chat_factory
from .commands import commands
from src.common.entities import Chat
from src.hub.hub import ai_hub

# 大模型核心类，负责管理个人助理agent流程
class _GenbanCore:
    def __init__(self):
        self.sessionManager = SessionManager()

    # 创建新会话，返回sessionId
    def newSession(self) -> str:
        return self.sessionManager.newSession()

    # 个人助理agent主流程，处理用户输入，返回流式输出
    def talk(self, sessionId, userInput):
        # 从会话管理器中获取对话状态和对话列表
        state = self.sessionManager.getState(sessionId)
        chats = self.sessionManager.getChats(sessionId)
        # 识别用户输入的指令，提取并执行
        commandResult, userInput = commands.handleCommand(state, userInput)
        if len(commandResult) > 0:
            yield chat_factory.createAssistantChat(commandResult)
        # 如果用户输入为空，则直接返回
        userInput = userInput.strip()
        if not userInput:
            return
        # 构建用户输入消息列表
        inputChats = chat_factory.createUserInputChats(
            isNewUser=len(chats) == 0, 
            userInput=userInput
        )
        # 执行循环，直到大模型不触发工具调用
        while True :
            chats.extend(inputChats)
            assistantChat = yield from self._call(chats=chats, model=state.model, enableThinking=state.deep_thinking)
            chats.append(assistantChat)
            if assistantChat.is_tool_call:
                print(assistantChat.message.tool_calls)
                inputChats = self._handleToolCalls(assistantChat.message.tool_calls)
                yield from inputChats
            else:
                break

    # 调用大模型接口，获取流式输出，return值为最后一个输出的Chat对象
    def _call(self, chats, model, enableThinking) -> Chat:
        responses = ai_hub.call(
            messages=chat_factory.adaptMessages(chats), 
            model=model, 
            tools=tool_caller.getTools(),
            enableThinking=enableThinking
        )
        lastChat = None
        for r in responses:
            if r.finish_reason == "length":
                raise CallHubLengthLimitedException()
            lastChat = chat_factory.createResponseChat(r)
            yield lastChat
        return lastChat

    # 处理工具调用，返回工具调用消息列表
    def _handleToolCalls(self, toolCalls) -> list[Chat]:
        toolChats = []
        for toolCall in toolCalls:
            # 进行工具调用获取结果
            toolResult = tool_caller.callTool(toolCall)
            # 构建工具调用消息列表
            toolChats.append(
                chat_factory.createToolCallChat(
                    toolCallId=toolCall['id'], 
                    toolResult=toolResult
                )
            )
        return toolChats

genban_core = _GenbanCore()
