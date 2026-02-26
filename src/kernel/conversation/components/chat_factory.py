from src.config.config import prompts
from src.common.entities import Message, Chat, CallResponse
from src.common.utils import time_util

class ChatFactory:

    def __init__(self):
        self.currentTime = time_util.getTimestamp()
        self.index = 0

    def _createChatId(self) -> str:
        if (time_util.getTimestamp() != self.currentTime):
            self.currentTime = time_util.getTimestamp()
            self.index = 0
        
        self.index += 1
        return f"{self.currentTime}{self.index:04d}"

    # 创建Message对象
    def createSystemMessage(self) -> Message:
        return Message(role="system", content=prompts.get("system_content"))

    def createUserMessage(self, userInput) -> Message:
        return Message(role="user", content=userInput)

    def createToolMessage(self, toolCallId, toolResult) -> Message:
        return Message(role="tool", tool_call_id=toolCallId, content=toolResult)

    def createAssistantMessage(self, content) -> Message:
        return Message(role="assistant", content=content)

    # 创建Chat对象
    def createPromptChat(self) -> Chat:
        return Chat(source="prompt", id=self._createChatId(), message=self.createSystemMessage())

    def createUserChat(self, userInput) -> Chat:
        return Chat(source="user", id=self._createChatId(), message=self.createUserMessage(userInput=userInput))

    def createToolChat(self, toolCallId, toolResult) -> Chat:
        return Chat(source="tool", id=self._createChatId(), message=self.createToolMessage(toolCallId=toolCallId, toolResult=toolResult))

    def createCommandChats(self, commandResults) -> list:
        return [Chat(source="command", id=self._createChatId(), message=self.createAssistantMessage(content=content)) for content in commandResults]

    # 根据大模型返回的响应，创建响应的Chat对象
    def createAssistantChat(self, response : CallResponse) -> Chat: 
        return Chat(
            source="assistant",
            message=response.message,
            id=response.request_id,
            total_tokens=response.total_tokens
        )

    # 根据是否是新用户和用户输入，创建用户输入的Chat列表
    def createUserInputChats(self, isNewUser, userInput) -> list:
        chats = []
        if isNewUser:
            chats.append(self.createPromptChat())
        chats.append(self.createUserChat(userInput=userInput))
        return chats

chatFactory = ChatFactory()