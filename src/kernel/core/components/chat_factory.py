from src.config.config import Prompts
from src.common.entities import Message, Chat, CallResponse
    
def createSystemMessage() -> Message:
    return Message(role="system", content=Prompts["system_content"])

def createUserMessage(userInput) -> Message:
    return Message(role="user", content=userInput)

def createChat(message : Message) -> Chat:
    chat = Chat()
    chat.message = message
    return chat

def createSystemChat() -> Chat:
    return createChat(createSystemMessage())

def createUserInputChat(userInput) -> Chat:
    return createChat(createUserMessage(userInput=userInput))

# 根据是否是新用户和用户输入，创建用户输入的Chat列表
def createUserInputChats(isNewUser, userInput) -> list:
    chats = []
    if isNewUser:
        chats.append(createSystemChat())
    chats.append(createUserInputChat(userInput=userInput))
    return chats

# 根据大模型返回的响应，创建响应的Chat对象
def createResponseChat(response : CallResponse) -> Chat:
    chat = createChat(response.message)
    chat.finishReason = response.finishReason
    chat.totalTokens = response.totalTokens
    return chat

# 合并旧信息和用户输入，返回调用大模型的消息列表
def buildMessages(oldMessages, userInputChats):
    for chat in userInputChats:
        oldMessages.append(chat.message)
    return adaptMessages(oldMessages)

def adaptMessages(messages) -> list:
    ms = []
    for m in messages:
        ms.append(m.__dict__)
    return ms