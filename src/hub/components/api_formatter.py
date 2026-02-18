from src.common.entities import Message, CallResponse

def messageFormat(choice) -> Message:
    message = choice.message
    m = Message("assistant")
    if 'content' in message:
        m.content = message.content
    if 'reasoning_content' in message:
        m.reasoningContent = message.reasoning_content
    if ('tool_calls' in message) and (message.tool_calls is not None):
        if (m.toolCalls is None):
            m.toolCalls=[]
        for t in message.tool_calls:
            m.toolCalls.append(t)
    return m

def dashScopeResponseFormat(response) -> CallResponse:
    chat = CallResponse()
    chat.statusCode = response.status_code
    chat.totalTokens = response.usage.total_tokens

    choice = response.output.choices[0]
    chat.finishReason = choice.finish_reason
    chat.message = messageFormat(choice)
    return chat
