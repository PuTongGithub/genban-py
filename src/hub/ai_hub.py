from .api import api_dash_scope
from .api import api_formatter
from .session.session_manager import SessionManager
from .message import message_factory

class _AiHub:

    def __init__(self):
        self.sessionManager = SessionManager()

    def newSession(self):
        return self.sessionManager.newSession()
    
    def _buildMessages(self, sessionId, userInput):
        messages = self.sessionManager.getMessages(sessionId=sessionId)
        if len(messages) == 0:
            ms = message_factory.createNewUserMessages(userInput=userInput)
            for m in ms:
                messages.append(m)
        else:
            messages.append(message_factory.createUserMessage(userInput=userInput))
        return message_factory.adaptMessages(messages)

    def talk(self, sessionId, userInput, model):
        messages = self._buildMessages(sessionId=sessionId, userInput=userInput)
        responses = api_dash_scope.call(model=model, messages=messages)
        newMessages = []
        for r in responses:
            m = api_formatter.dashScopeResponseFormat(r)
            yield m
            newMessages.append(m)
        
        newMessage = api_formatter.assembleResponseMessages(newMessages)
        self.sessionManager.addMessages(sessionId=sessionId, newMessages=[newMessage])
        
ai_hub = _AiHub()