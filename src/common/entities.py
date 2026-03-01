from dataclasses import dataclass, field
from enum import StrEnum, unique, Enum
from typing import Optional
from .utils import time_util

# 大模型消息实体
@dataclass
class Message:
    role: str = ""  # 角色: system, user, assistant, tool
    content: str = ""
    reasoning_content: str = ""
    tool_calls: Optional[list] = None
    tool_call_id: Optional[str] = None

@unique
class MessageRole(StrEnum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"

# 大模型接口调用返回值统一封装
@dataclass
class CallResponse:
    request_id: str
    status_code: int
    total_tokens: int
    finish_reason: str
    message: Message

# kernel模块针对对话内容的封装
@dataclass
class Chat:
    type: str = ""    # 对话类型: prompt, user, assistant, tool, command, memory, toolSummary
    id: str = ""    # 对话id，唯一键，升序排列
    override_id_begin: Optional[str] = None   # 覆盖起始id（包含），用当前Chat覆盖之前的对话内容
    override_id_end: Optional[str] = None   # 覆盖结束id（包含），用当前Chat覆盖之前的对话内容
    time: int = field(default_factory=time_util.getTimestamp)    # 对话时间，秒级时间戳
    total_tokens: int = 0   # 本次调用消耗的token数（仅source=assistant时有效）
    message: Optional[Message] = None  # 对话内容

@unique
class ChatType(Enum):
    PROMPT = ("prompt", False, True)
    USER = ("user", False, True)
    ASSISTANT = ("assistant", True, True)
    TOOL = ("tool", True, True)
    COMMAND = ("command", True, False)
    MEMORY = ("memory", False, True)
    TOOL_SUMMARY = ("toolSummary", False, True)
    ERROR = ("error", True, False)

    def __init__(self, value: str, userVisible: bool, assistantVisible: bool):
        self._value_ = value
        self.userVisible = userVisible
        self.assistantVisible = assistantVisible

chatTypeMap = {chatType.value: chatType for chatType in ChatType}