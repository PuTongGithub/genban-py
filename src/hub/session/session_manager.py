from .session_holder import SessionHolder
from .session_exception import *
from ...tools import time_util as TimeUtil
import random

class SessionManager:
    @staticmethod
    def _createId():
        return TimeUtil.getNowStr(TimeUtil.STR_FORMATTER_NO_MARKS) + str(random.randint(1, 1000))

    def __init__(self):
        self.sessions = {};
    
    def getHolder(self, sessionId):
        holder = self.sessions[sessionId]
        if holder == None:
            raise SessionIdNotFoundException(f"sessionId:{sessionId}")
        return holder
    
    def newSession(self):
        id = SessionManager._createId()
        holder = SessionHolder(sessionId=id)
        self.sessions[id] = holder
        return id

    def getMessages(self, sessionId):
        return self.getHolder(sessionId=sessionId).getMessages()

    def addMessages(self, sessionId, newMessages):
        self.getHolder(sessionId=sessionId).addMessages(newMessages)
