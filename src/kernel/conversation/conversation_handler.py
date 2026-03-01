import asyncio
import traceback
from src.common.entities import Chat
from src.common.exceptions import CallHubException, ConversationClosedException, CallHubLengthLimitedException
from src.common.async_executor import AsyncExecutor
from .components.chat_factory import chatFactory
from .conversation import Conversation
from ..memory.memory_manager import memoryManager
from ..invoker import invoker
from ..tools.tool_caller import toolCaller
from ..commands import commands
from src.user.user_manager import userManager

# 对话对象处理类，异步处理新产生的Chat
class ConversationHandler:

    def __init__(self, userId: str):
        self._userId = userId
        self._conversation = Conversation(userId=userId)
        self._newChatsQueue = asyncio.Queue()
        self._task = None
        
        # 创建执行器（自动启动），注册停止回调
        self._executor = AsyncExecutor(
            name=f"ConversationHandler-{userId}",
            on_stop=self._on_stop
        )
        self._task = self._executor.submit(self._execute())

    def _on_stop(self):
        """停止回调：发送停止信号并等待任务完成"""
        self._executor.submit(self._newChatsQueue.put(None))
        if self._task:
            self._task.result()
    
    # 订阅推送
    def subscribe(self) -> asyncio.Queue:
        return self._conversation.subscribe()
    
    # 取消订阅
    def unsubscribe(self, queue: asyncio.Queue):
        self._conversation.unsubscribe(queue)
    
    # 异步执行，循环拉取新对话进行处理
    async def _execute(self):
        while True:
            try:
                newChat = await self._newChatsQueue.get()
                if newChat is None:
                    break
                else:
                    self._handleNewChat(newChat)
            except Exception:
                traceback.print_exc()
                continue

    # 处理新对话
    def _handleNewChat(self, newChat: Chat):
        # todo: 调用大模型前：提示词注入、记忆召回
        
        # 执行大模型调用
        self._processNewChat(newChat)
        
        # TODO: 调用大模型后：对话持久化、工具总结、话题总结
        self._conversation.finishNewChat()
        

    # 执行新一轮的对话
    def _processNewChat(self, newChat: Chat):
        self._conversation.appendNewChat(newChat)
        try:
            state = userManager.getState(self._userId)
            # 执行循环，直到大模型不再触发工具调用
            while True :
                assistantChat = invoker.call(
                    chats=self._conversation.getAssistantChats(),
                    model=state.model, 
                    enableThinking=state.deep_thinking
                )
                self._conversation.appendNewChat(assistantChat)
                if assistantChat.message.tool_calls is not None:
                    inputChats = self._handleToolCalls(assistantChat.message.tool_calls)
                    self._conversation.extendNewChats(inputChats)
                else:
                    break;
        except CallHubLengthLimitedException:
            limitedChat = chatFactory.createErrorChat(content="本次执行内容过长，请重新输入。")
            self._conversation.submitErrorChat(limitedChat)
        except CallHubException as e:
            traceback.print_exc()
            errorChat = chatFactory.createErrorChat(content=str(e))
            self._conversation.submitErrorChat(errorChat)

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

    # 提交新的对话到待执行队列
    def submitNewChat(self, chat: Chat):
        if not self._executor:
            raise ConversationClosedException()
        self._executor.submit(self._newChatsQueue.put(chat))

    # 提交用户输入
    def submitUserInput(self, userInput: str) -> str:
        # 识别用户输入的指令，提取并执行
        userInput, commandChats = self._handleCommand(userInput)
        if len(commandChats) > 0:
            self._conversation.submitCommandChats(commandChats)
        if not userInput:
            return ""

        userChat = chatFactory.createUserChat(userId=self._userId, userInput=userInput)
        self.submitNewChat(userChat)
        return userChat.id

    # 处理用户输入包含的指令，返回去掉指令的用户输入和指令结果列表
    def _handleCommand(self, userInput) -> tuple[str, list[Chat]]:
        state = userManager.getState(self._userId)
        commandResults, userInput, stateChanged = commands.handleCommand(state, userInput)
        commandChats = []
        if len(commandResults) > 0:
            commandChats = chatFactory.createCommandChats(commandResults)
        if stateChanged:
            userManager.updateState(state)
        return userInput, commandChats
