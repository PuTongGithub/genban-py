from dataclasses import dataclass

# 大模型消息实体
@dataclass
class Message:
    role: str = ""
    content: str = ""
    reasoning_content: str = ""
    tool_calls: list = None

# 大模型接口调用返回值统一封装
@dataclass
class Chat:
    statusCode: int = 0
    totalTokens: int = 0
    finish_reason: str = ""
    message: Message = None
