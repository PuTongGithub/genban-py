from dataclasses import dataclass
from .utils import time_util

# 大模型消息实体
@dataclass
class Message:
    role: str = ""
    content: str = ""
    reasoning_content: str = ""
    tool_calls: list = None
    tool_call_id: str = None

# 大模型接口调用返回值统一封装
@dataclass
class CallResponse:
    status_code: int = 0
    total_tokens: int = 0
    finish_reason: str = ""
    message: Message = None

# kernel模块针对对话内容的封装
@dataclass
class Chat:
    total_tokens: int = 0
    is_tool_call: bool = False
    message: Message = None
    time: str = time_util.getNowStr(time_util.STR_FORMATTER_WITH_MARKS)