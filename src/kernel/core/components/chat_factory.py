from src.config.config import prompts
from src.common.entities import Message, Chat, CallResponse
import uuid

# 创建Message对象
def createSystemMessage() -> Message:
    return Message(role="system", content=prompts.get("system_content"))

def createUserMessage(userInput) -> Message:
    return Message(role="user", content=userInput)

def createToolMessage(toolCallId, toolResult) -> Message:
    return Message(role="tool", tool_call_id=toolCallId, content=toolResult)

def createAssistantMessage(content) -> Message:
    return Message(role="assistant", content=content)

# 创建Chat对象
def createPromptChat() -> Chat:
    return Chat(source="prompt", id=str(uuid.uuid4()), message=createSystemMessage())

def createUserChat(userInput) -> Chat:
    return Chat(source="user", id=str(uuid.uuid4()), message=createUserMessage(userInput=userInput))

def createToolChat(toolCallId, toolResult) -> Chat:
    return Chat(source="tool", id=str(uuid.uuid4()), message=createToolMessage(toolCallId=toolCallId, toolResult=toolResult))

def createCommandChats(commandResults) -> list:
    return [Chat(source="command", id=str(uuid.uuid4()), message=createAssistantMessage(content=content)) for content in commandResults]

# 根据大模型返回的响应，创建响应的Chat对象
def createAssistantChat(response : CallResponse) -> Chat:
    return Chat(
        source="assistant",
        message=response.message,
        id=response.request_id,
        total_tokens=response.total_tokens
    )

# 根据是否是新用户和用户输入，创建用户输入的Chat列表
def createUserInputChats(isNewUser, userInput) -> list:
    chats = []
    if isNewUser:
        chats.append(createPromptChat())
    chats.append(createUserChat(userInput=userInput))
    return chats