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
    source: str = ""    # 对话来源: prompt, user, assistant, tool, command, memory
    id: str = ""    # 对话id，唯一键，升序排列
    override_id_begin: str = None   # 覆盖起始id（包含），用当前Chat覆盖之前的对话内容
    override_id_end: str = None   # 覆盖结束id（包含），用当前Chat覆盖之前的对话内容
    time: int = time_util.getTimestamp()    # 对话时间，秒级时间戳
    message: Message = None # 对话内容
    total_tokens: int = 0   # 本次调用消耗的token数（仅source=assistant时有效）
