from ..session.session_manager import SessionManager
from ...hub.hub import ai_hub
import asyncio

class _GenbanCore:
    def __init__(self):
        self.sessionManager = SessionManager()

    def newSession(self):
        return self.sessionManager.newSession()

    def talk(self, sessionId, userInput, model):
        # 从会话管理器中获取旧消息
        oldMessages = self.sessionManager.getMessages(sessionId)
        # 调用大模型接口，获取流式输出  
        chats = ai_hub.chat(oldMessages=oldMessages, userInput=userInput, model=model)
        # 遍历流式输出，返回每个Chat对象
        lastChat = None
        for c in chats:
            lastChat = c
            yield c.message
        # 如果最后一个Chat对象不为空，将其消息添加到会话管理器中
        if lastChat is not None:
            asyncio.run(self.asyncAddMessages(sessionId=sessionId, newMessages=[lastChat.message]))

    async def asyncAddMessages(self, sessionId, newMessages):
        self.sessionManager.addMessages(sessionId=sessionId, newMessages=newMessages)

genban_core = _GenbanCore()
