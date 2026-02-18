from src.common.exceptions import SessionIdNotFoundException
from src.common.utils import time_util as TimeUtil
import random

class SessionManager:
    @staticmethod
    def _createId():
        return TimeUtil.getNowStr(TimeUtil.STR_FORMATTER_NO_MARKS) + str(random.randint(1, 1000))

    def __init__(self):
        self.chatsMap = {}
    
    def newSession(self) -> str:
        id = SessionManager._createId()
        self.chatsMap[id] = []
        return id
    
    def getChats(self, sessionId: str) -> list[Chat]:
        chats = self.chatsMap[sessionId]
        if chats == None:
            raise SessionIdNotFoundException(sessionId)
        return chats

    def addChat(self, sessionId, newChat):
        self.getChats(sessionId=sessionId).append(newChat)

    def addChats(self, sessionId, newChats):
        self.getChats(sessionId=sessionId).extend(newChats)
