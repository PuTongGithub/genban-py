from src.config.config import prompts
from src.common.entities import Message, Chat, CallResponse
    
def createSystemMessage() -> Message:
    return Message(role="system", content=prompts.get("system_content"))

def createUserMessage(userInput) -> Message:
    return Message(role="user", content=userInput)

def createAssistantMessage(content) -> Message:
    return Message(role="assistant", content=content)

def createToolMessage(toolCallId, toolResult) -> Message:
    return Message(role="tool", tool_call_id=toolCallId, content=toolResult)

def createChat(message : Message) -> Chat:
    chat = Chat()
    chat.message = message
    return chat

def createSystemChat() -> Chat:
    return createChat(createSystemMessage())

def createUserInputChat(userInput) -> Chat:
    return createChat(createUserMessage(userInput=userInput))

def createAssistantChat(content) -> Chat:
    return createChat(createAssistantMessage(content=content))

def createToolCallChat(toolCallId, toolResult) -> Chat:
    chat = createChat(createToolMessage(toolCallId=toolCallId, toolResult=toolResult))
    print(chat)
    return chat

# 根据是否是新用户和用户输入，创建用户输入的Chat列表
def createUserInputChats(isNewUser, userInput) -> list:
    chats = []
    if isNewUser:
        chats.append(createSystemChat())
    chats.append(createUserInputChat(userInput=userInput))
    print(chats)
    return chats

# 根据大模型返回的响应，创建响应的Chat对象
def createResponseChat(response : CallResponse) -> Chat:
    chat = createChat(response.message)
    chat.total_tokens = response.total_tokens
    chat.is_tool_call = response.finish_reason == "tool_calls"
    return chat

# 转换消息列表为大模型调用的格式
def adaptMessages(chats : list[Chat]) -> list:
    ms = []
    for chat in chats:
        m = chat.message
        mdict = {}
        mdict["role"] = m.role
        mdict["content"] = m.content
        if m.tool_calls is not None:
            mdict["tool_calls"] = m.tool_calls
        if m.tool_call_id is not None:
            mdict["tool_call_id"] = m.tool_call_id
        ms.append(mdict)
    return ms