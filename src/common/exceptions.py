class SessionIdNotFoundException(Exception):
    def __init__(self, sessionId: str):
        super().__init__(f"sessionId:{sessionId} not found")

class CallHubException(Exception):
    def __init__(self, message: str):
        super().__init__(message)

class CallHubLengthLimitedException(Exception):
    def __init__(self):
        super().__init__("call hub length limited")

class ToolNotExistException(Exception):
    def __init__(self, toolName: str):
        super().__init__(f"tool:{toolName} not found")
