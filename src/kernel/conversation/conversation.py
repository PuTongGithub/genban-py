from typing import List
from src.common.entities import Chat
from src.kernel.memory.memory_manager import memoryManager

# 对话对象类
class Conversation:

    def __init__(self, userId: str):
        self.userId = userId
        self.chats = memoryManager.getChats(userId)
        self.newChats = []

    def extend(self, chats: List[Chat]):
        self.chats.extend(chats)
        self.newChats.extend(chats)

    def append(self, chat: Chat):
        self.chats.append(chat)
        self.newChats.append(chat)

    # 结束对话, 追加新增的用户对话到记忆中
    def finishTalk(self):
        memoryManager.appendChats(self.userId, self.newChats)
        self.newChats = []
        