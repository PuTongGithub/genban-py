from typing import Optional
from pydantic import BaseModel


class SubmitRequest(BaseModel):
    user_input: str = ""

class SubmitResponse(BaseModel):
    chat_id: str = ""

class TalkResponse(BaseModel):
    type: str = ""  # 消息类型，assistant/tool/command/error
    id: str = ""  # 消息ID
    role: str = ""  # 消息角色，assistant/tool
    content: str = ""  # 消息内容
    reasoning_content: str = ""  # 推理内容
    tool_calls: Optional[list] = None  # 工具调用列表

class QueryRequest(BaseModel):
    start_id: str = ""

class QueryResponse(BaseModel):
    chats: list[TalkResponse] = []

class LoginRequest(BaseModel):
    user_id: str = ""
    password: str = ""

class LoginResponse(BaseModel):
    token: Optional[str] = ""
    expires_at: Optional[int] = 0
    error: Optional[str] = ""
