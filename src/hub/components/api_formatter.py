from ..entities import Message, Chat

def messageFormat(choice) -> Message:
    m = Message("assistant")
    if 'content' in choice.message:
        m.content = choice.message.content
    if 'reasoning_content' in choice.message:
        m.reasoning_content = choice.message.reasoning_content
    if ('tool_calls' in choice.message) and (choice.message.tool_calls != None):
        if (m.tool_calls == None):
            m.tool_calls=[]
        for t in choice.message.tool_calls:
            m.tool_calls.append(t)
    return m

def dashScopeResponseFormat(response) -> Chat:
    chat = Chat()
    chat.statusCode = response.status_code
    chat.totalTokens = response.usage.total_tokens

    choice = response.output.choices[0]
    chat.finish_reason = choice.finish_reason
    chat.message = messageFormat(choice)
    return chat
