from pydantic import BaseModel

class TalkRequest(BaseModel):
    session_id: str = ""
    user_input: str = ""
    model: str = ""

class TalkResponse(BaseModel):
    role: str = ""
    content: str = ""
    reasoning_content: str = ""
