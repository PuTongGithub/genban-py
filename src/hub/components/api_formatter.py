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

    choice = response.output.choices[0]
    chat.finish_reason = choice.finish_reason
    chat.message = messageFormat(choice)
    return chat
