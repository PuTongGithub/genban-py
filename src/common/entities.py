from dataclasses import dataclass
from .utils import time_util

# 大模型消息实体
@dataclass
class Message:
    role: str = ""  # 角色: system, user, assistant, tool
    content: str = ""
    reasoning_content: str = ""
    tool_calls: list = None
    tool_call_id: str = None

# 大模型接口调用返回值统一封装
@dataclass
class CallResponse:
    request_id: str = ""
    status_code: int = 0
    total_tokens: int = 0
    finish_reason: str = ""
    message: Message = None

# kernel模块针对对话内容的封装
@dataclass
class Chat:
    source: str = ""    # 对话来源: prompt, user, assistant, tool, command
    id: str = ""
    total_tokens: int = 0
    message: Message = None
    time: str = time_util.getNowStr(time_util.STR_FORMATTER_WITH_MARKS)