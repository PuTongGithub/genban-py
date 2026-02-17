from dataclasses import dataclass
from .utils import time_util

# 大模型消息实体
@dataclass
class Message:
    role: str = ""
    content: str = ""
    reasoning_content: str = ""
    tool_calls: list = None

# 大模型接口调用返回值统一封装
@dataclass
class CallResponse:
    statusCode: int = 0
    totalTokens: int = 0
    finishReason: str = ""
    message: Message = None

@dataclass
class Chat:
    totalTokens: int = 0
    finishReason: str = ""
    message: Message = None
    time: str = time_util.getNowStr(time_util.STR_FORMATTER_WITH_MARKS)