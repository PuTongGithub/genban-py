from .session_exception import *
from src.common.utils import time_util as TimeUtil
import random

class SessionManager:
    @staticmethod
    def _createId():
        return TimeUtil.getNowStr(TimeUtil.STR_FORMATTER_NO_MARKS) + str(random.randint(1, 1000))

    def __init__(self):
        self.chatsMap = {}
    
    def newSession(self):
        id = SessionManager._createId()
        self.chatsMap[id] = []
        return id
    
    def getChats(self, sessionId):
        chats = self.chatsMap[sessionId]
        if chats == None:
            raise SessionIdNotFoundException(f"sessionId:{sessionId}")
        return chats

    def getMessages(self, sessionId):
        chats = self.getChats(sessionId=sessionId)
        messages = []
        for chat in chats:
            messages.append(chat.message)
        return messages

    def addChat(self, sessionId, newChat):
        self.getChats(sessionId=sessionId).append(newChat)

    def addChats(self, sessionId, newChats):
        self.getChats(sessionId=sessionId).extend(newChats)
