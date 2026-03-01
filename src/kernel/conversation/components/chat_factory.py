from src.common.entities import Message, Chat, CallResponse, MessageRole, ChatType
from src.common.utils import time_util

class _ChatFactory:

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
    def createSystemMessage(self, content) -> Message:
        return Message(role=MessageRole.SYSTEM.value, content=content)

    def createUserMessage(self, userId, userInput) -> Message:
        time = time_util.getNowStr(time_util.STR_FORMATTER_WITH_MARKS)
        return Message(role=MessageRole.USER.value, content=f"[user:{userId}:{time}]"+userInput)

    def createToolMessage(self, toolCallId, toolResult) -> Message:
        return Message(role=MessageRole.TOOL.value, tool_call_id=toolCallId, content=toolResult)

    def createAssistantMessage(self, content) -> Message:
        return Message(role=MessageRole.ASSISTANT.value, content=content)

    def createDefaultMessage(self, content) -> Message:
        return Message(role=MessageRole.USER.value, content=content)

    # 创建Chat对象
    def createPromptChat(self, content) -> Chat:
        return Chat(type=ChatType.PROMPT.value, id=self._createChatId(), message=self.createSystemMessage(content=content))

    def createUserChat(self, userId, userInput) -> Chat:
        return Chat(type=ChatType.USER.value, id=self._createChatId(), message=self.createUserMessage(userId=userId, userInput=userInput))

    def createToolChat(self, toolCallId, toolResult) -> Chat:
        return Chat(type=ChatType.TOOL.value, id=self._createChatId(), message=self.createToolMessage(toolCallId=toolCallId, toolResult=toolResult))

    def createCommandChats(self, commandResults) -> list:
        return [Chat(type=ChatType.COMMAND.value, id=self._createChatId(), message=self.createAssistantMessage(content=content)) for content in commandResults]

    def createErrorChat(self, content) -> Chat:
        return Chat(type=ChatType.ERROR.value, id=self._createChatId(), message=self.createDefaultMessage(content=content))

    # 根据大模型返回的响应，创建响应的Chat对象
    def createAssistantChat(self, response : CallResponse) -> Chat: 
        return Chat(
            type=ChatType.ASSISTANT.value,
            id=self._createChatId(),
            message=response.message,
            total_tokens=response.total_tokens
        )

chatFactory = _ChatFactory()