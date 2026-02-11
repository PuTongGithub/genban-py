class Message:

    def __init__(self, role="", content="", reasoning_content="", tool_calls=None):
        self.role = role
        self.content = content
        self.reasoning_content = reasoning_content
        self.tool_calls = tool_calls

    def __str__(self):
        return f"\"role\":{self.role}, \"content\":{self.content}, \"reasoning_content\":{self.reasoning_content}, \"tool_calls\":{self.tool_calls}"
    