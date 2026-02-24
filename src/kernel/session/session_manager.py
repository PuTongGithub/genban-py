from src.common.exceptions import SessionIdNotFoundException
from src.common.utils import time_util as TimeUtil
from src.config.config import app_config
import random

class SessionState:
    def __init__(self, model: str):
        self.deep_thinking: bool = False
        self.model: str = model

class SessionManager:
    @staticmethod
    def _createId():
        return TimeUtil.getNowStr(TimeUtil.STR_FORMATTER_NO_MARKS) + str(random.randint(1, 1000))

    def __init__(self):
        self.chatsMap = {}
        self.stateMap = {}
    
    def newSession(self) -> str:
        id = SessionManager._createId()
        self.chatsMap[id] = []
        self.stateMap[id] = SessionState(model=app_config.getDefaultModel())
        return id
    
    def getChats(self, sessionId: str) -> list:
        chats = self.chatsMap.get(sessionId)
        if chats is None:
            raise SessionIdNotFoundException(sessionId)
        return chats

    def addChat(self, sessionId, newChat):
        self.getChats(sessionId=sessionId).append(newChat)

    def addChats(self, sessionId, newChats):
        self.getChats(sessionId=sessionId).extend(newChats)
    
    def getState(self, sessionId: str) -> SessionState:
        state = self.stateMap.get(sessionId)
        if state is None:
            raise SessionIdNotFoundException(sessionId)
        return state
