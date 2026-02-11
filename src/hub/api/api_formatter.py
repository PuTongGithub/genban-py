from ..message.message import Message

def dashScopeResponseFormat(response):
    cs = response.output.choices
    m = Message("assistant")
    for c in cs:
        message = c.message
        if 'content' in message:
            m.content += message.content
        if 'reasoning_content' in message:
            m.reasoning_content += message.reasoning_content
        if ('tool_calls' in message) and (message.tool_calls != None):
            if (m.tool_calls == None):
                m.tool_calls=[]
            for t in message.tool_calls:
                m.tool_calls.append(t)
    return m

def assembleResponseMessages(messages):
    if len(messages) == 0 :
        return Message()
    
    m = Message(messages[0].role)
    for message in messages:
        m.content += message.content
        m.reasoning_content += message.reasoning_content
        if message.tool_calls != None:
            if (m.tool_calls == None):
                m.tool_calls=[]
            for t in message.tool_calls:
                m.tool_calls.append(t)
    
    return m