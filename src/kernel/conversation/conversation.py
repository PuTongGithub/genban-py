import asyncio
from typing import Set
from readerwriterlock import rwlock
from src.common.entities import Chat, ChatType, chatTypeMap
from src.common.exceptions import SubmitCommandChatsException
from src.common.async_executor import AsyncExecutor
from src.config.prompts_loader import promptsLoader
from ..memory.memory_manager import memoryManager
from .components.chat_factory import chatFactory

# 对话对象类，维护对话记录，主动向订阅者推送新对话
class Conversation:

    def __init__(self, userId):
        self._uid = userId
        self._chats = memoryManager.getChats(userId)
        self._promptChat = chatFactory.createPromptChat(content=promptsLoader.getStewardPrompt())
        self._newChats = []
        self._rwlock = rwlock.RWLockFair()
        # SSE 推送订阅者集合
        self._subscribers: Set[asyncio.Queue] = set()
        # 创建独立的广播执行器
        self._broadcast_executor = AsyncExecutor(name=f"Broadcast-{userId}")
    
    # 创建广播任务，将新对话推送到所有订阅者
    def _createBroadcastTask(self, chat: Chat):
        self._broadcast_executor.submit(self._broadcastChat(chat))

    # 向所有订阅者推送消息
    async def _broadcastChat(self, chat: Chat):
        for queue in list(self._subscribers):
            try:
                await queue.put(chat)
            except Exception:
                self._subscribers.discard(queue)
    
    # 订阅 SSE 推送，返回消息队列
    def subscribe(self) -> asyncio.Queue:
        queue = asyncio.Queue()
        self._subscribers.add(queue)
        return queue
    
    # 取消订阅
    def unsubscribe(self, queue: asyncio.Queue):
        self._subscribers.discard(queue)

    # 获取助手可见的对话列表
    def getAssistantChats(self) -> list[Chat]:
        with self._rwlock.gen_rlock():
            assistantChats = [self._promptChat]
            for chat in self._chats:
                if chatTypeMap[chat.type].assistantVisible:
                    assistantChats.append(chat)
            return assistantChats

    # 提交命令对话，将其广播到所有订阅者
    def submitCommandChats(self, commandChats: list[Chat]):
        for chat in commandChats:
            if chat.type != ChatType.COMMAND.value:
                raise SubmitCommandChatsException()
        with self._rwlock.gen_wlock():
            for chat in commandChats:
                self._createBroadcastTask(chat)

    # 提交错误对话，将其广播到所有订阅者
    def submitErrorChat(self, errorChat: Chat):
        if errorChat.type != ChatType.ERROR.value:
            raise SubmitCommandChatsException()
        with self._rwlock.gen_wlock():
            self._createBroadcastTask(errorChat)

    # 向新对话列表添加新对话，并广播到所有订阅者
    def appendNewChat(self, newChat: Chat):
        with self._rwlock.gen_wlock():
            self._chats.append(newChat)
            self._newChats.append(newChat)
            self._createBroadcastTask(newChat)

    def extendNewChats(self, newChats: list[Chat]):
        with self._rwlock.gen_wlock():
            self._chats.extend(newChats)
            self._newChats.extend(newChats)
            for chat in newChats:
                self._createBroadcastTask(chat)

    # 合并新对话到主对话列表，会将新对话写入记忆系统
    def finishNewChat(self):
        with self._rwlock.gen_wlock():
            memoryManager.appendChats(self._uid, self._newChats)
            self._newChats = []

