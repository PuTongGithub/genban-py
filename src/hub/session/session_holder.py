from ...tools import time_util as TimeUtil

class SessionHolder:

    def __init__(self, sessionId):
        self.id = sessionId
        self.messages = []
        self.timestamp = TimeUtil.getTimestamp()

    def __str__(self):
        return f"""SessionHolder: id-{self.id} 
        message-
        {self.messages}
        """
    
    def getId(self):
        return self.id
    
    def getMessages(self):
        return self.messages
    
    def addMessages(self, newMessages):
        for m in newMessages:
            self.messages.append(m)
        self.timestamp = TimeUtil.getTimestamp()

    def checkExpire(self, expireTimestamp):
        return TimeUtil.getTimestamp() - self.timestamp > expireTimestamp