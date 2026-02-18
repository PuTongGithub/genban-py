from pydantic import BaseModel

class TalkRequest(BaseModel):
    sessionId: str = ""
    userInput: str = ""
    model: str = ""

class TalkResponse(BaseModel):
    role: str = ""
    content: str = ""
    reasoning_content: str = ""
