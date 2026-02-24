from src.common.entities import Message, CallResponse

def messageFormat(choice) -> Message:
    message = choice.message
    m = Message(role=message.role, content=message.content)
    if 'reasoning_content' in message:
        m.reasoning_content = message.reasoning_content
    if ('tool_calls' in message) and (message.tool_calls is not None):
        if (m.tool_calls is None):
            m.tool_calls=[]
        for t in message.tool_calls:
            m.tool_calls.append(t)
    return m

def dashScopeResponseFormat(response) -> CallResponse:
    chat = CallResponse()
    chat.status_code = response.status_code
    chat.total_tokens = response.usage.total_tokens
    chat.request_id = response.request_id
    
    choice = response.output.choices[0]
    chat.finish_reason = choice.finish_reason
    chat.message = messageFormat(choice)
    return chat


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