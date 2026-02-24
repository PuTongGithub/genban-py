from pydantic import BaseModel

class TalkRequest(BaseModel):
    session_id: str = ""
    user_input: str = ""

class TalkResponse(BaseModel):
    source: str = "" # 消息来源，assistant/tool/command
    id: str = "" # 消息ID
    role: str = "" # 消息角色，assistant/tool
    content: str = "" # 消息内容
    reasoning_content: str = "" # 推理内容
    tool_calls: list = None # 工具调用列表
