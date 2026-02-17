from ..session.session_manager import SessionManager
from src.hub.hub import ai_hub
from .components import chat_factory
import asyncio

class _GenbanCore:
    def __init__(self):
        self.sessionManager = SessionManager()

    def newSession(self):
        return self.sessionManager.newSession()

    def talk(self, sessionId, userInput, model):
        # 从会话管理器中获取旧消息，结合用户输入，构建调用大模型的消息列表
        oldMessages = self.sessionManager.getMessages(sessionId)
        userInputChats = chat_factory.createUserInputChats(isNewUser=len(oldMessages) == 0, userInput=userInput)
        messages = chat_factory.buildMessages(oldMessages, userInputChats)
        # 调用大模型接口，获取流式输出  
        responses = ai_hub.call(messages=messages, model=model)
        # 遍历流式输出，返回每个Chat对象
        lastChat = None
        for r in responses:
            lastChat = chat_factory.createResponseChat(r)
            yield lastChat.message
        # 如果最后一个Chat对象不为空，将其消息添加到会话管理器中
        if lastChat is not None:
            asyncio.run(self.asyncAddChats(sessionId=sessionId, userInputChats=userInputChats, newChat=lastChat))

    async def asyncAddChats(self, sessionId, userInputChats, newChat):
        userInputChats.append(newChat)
        self.sessionManager.addChats(sessionId=sessionId, newChats=userInputChats)

genban_core = _GenbanCore()
