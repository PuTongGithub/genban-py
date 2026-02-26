from ..tools.tool_caller import toolCaller
from ..conversation.components.chat_factory import chatFactory
from ..conversation.conversation_manager import conversationHolder
from .commands import commands
from src.common.entities import Chat
from src.hub.hub import aiHub
from src.user.user_manager import userManager

# 大模型核心类，负责管理个人助理agent流程
class _GenbanCore:

    # 个人助理agent主流程，处理用户输入，返回流式输出
    def talk(self, userId, userInput):
        # 从用户管理器中获取用户状态
        state = userManager.getState(userId)
        # 识别用户输入的指令，提取并执行
        userInput = yield from self._handleCommand(state, userInput)
        # 如果用户输入为空，则直接返回
        if not userInput:
            return

        # 从对话管理器中获取用户对话对象
        conversation = conversationHolder.getConversation(userId, userInput)
        # 执行循环，直到大模型不再触发工具调用
        while True :
            assistantChat = yield from self._call(chats=conversation.chats, model=state.model, enableThinking=state.deep_thinking)
            conversation.append(assistantChat)
            if assistantChat.message.tool_calls is not None:
                inputChats = self._handleToolCalls(assistantChat.message.tool_calls)
                conversation.extend(inputChats)
                yield from inputChats
            else:
                break
        # 结束对话
        conversation.finishTalk()

    # 处理用户输入包含的指令，返回处理结果字符串列表以及去掉指令的用户输入
    def _handleCommand(self, state, userInput) -> str:
        commandResults, userInput, stateChanged = commands.handleCommand(state, userInput)
        if len(commandResults) > 0:
            yield from chatFactory.createCommandChats(commandResults)
        if stateChanged:
            userManager.updateState(state)
        return userInput

    # 调用大模型接口，获取流式输出，return值为最后一个输出的Chat对象
    def _call(self, chats, model, enableThinking) -> Chat:
        responses = aiHub.call(
            chats=chats, 
            model=model, 
            tools=toolCaller.getTools(),
            enableThinking=enableThinking
        )
        lastChat = None
        for r in responses:
            if r.finish_reason == "length":
                raise CallHubLengthLimitedException()
            lastChat = chatFactory.createAssistantChat(r)
            yield lastChat
        return lastChat

    # 处理工具调用，返回工具调用消息列表
    def _handleToolCalls(self, toolCalls) -> list[Chat]:
        toolChats = []
        for toolCall in toolCalls:
            # 进行工具调用获取结果
            toolResult = toolCaller.callTool(toolCall)
            # 构建工具调用消息列表
            toolChats.append(
                chatFactory.createToolChat(
                    toolCallId=toolCall['id'], 
                    toolResult=toolResult
                )
            )
        return toolChats

genbanCore = _GenbanCore()
