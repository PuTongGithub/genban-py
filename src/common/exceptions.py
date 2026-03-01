class EnvConfigNotFoundException(Exception):
    def __init__(self, key: str):
        super().__init__(f"env config:{key} not found")

class UserIdNotFoundException(Exception):
    def __init__(self, userId: str):
        super().__init__(f"userId:{userId} not found")

class CallHubException(Exception):
    def __init__(self, message: str):
        super().__init__(message)

class CallHubLengthLimitedException(Exception):
    def __init__(self):
        super().__init__("call hub length limited")

class ToolNotExistException(Exception):
    def __init__(self, toolName: str):
        super().__init__(f"tool:{toolName} not found")

class ModelNotFoundException(Exception):
    def __init__(self, modelName: str):
        super().__init__(f"model:{modelName} not found")


class UserNotFoundException(Exception):
    def __init__(self, userId: str):
        super().__init__(f"user:{userId} not found")


class InvalidPasswordException(Exception):
    def __init__(self):
        super().__init__("invalid password")

class UnauthorizedException(Exception):
    def __init__(self):
        super().__init__("unauthorized")

class ConversationClosedException(Exception):
    def __init__(self):
        super().__init__("conversation closed")

class SubmitCommandChatsException(Exception):
    def __init__(self):
        super().__init__("submit command chats failed")