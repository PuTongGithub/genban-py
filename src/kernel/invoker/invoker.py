from src.hub.hub import aiHub
from src.common.exceptions import CallHubLengthLimitedException
from ..conversation.components.chat_factory import chatFactory
from ..tools.tool_caller import toolCaller

# 转换Chat列表为大模型调用的格式
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

# 调用大模型接口获取结果，返回Chat对象
def call(chats, model, enableThinking):
    response = aiHub.call(
        messages=adaptMessages(chats), 
        model=model, 
        tools=toolCaller.getTools(),
        enableThinking=enableThinking
    )
    
    if response.finish_reason == "length":
        raise CallHubLengthLimitedException()
        
    return chatFactory.createAssistantChat(response)
