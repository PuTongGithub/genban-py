import json
from pydantic import BaseModel
from ...hub.entities import Message

class TalkRequest(BaseModel):
    sessionId: str = ""
    userInput: str = ""
    model: str = ""

class TalkResponse(BaseModel):
    role: str = ""
    content: str = ""
    reasoning_content: str = ""

def adaptTalkResponse(message:Message):
    res = TalkResponse()
    res.role = message.role
    res.content = message.content
    res.reasoning_content = message.reasoning_content
    return f"data:{json.dumps(res.model_dump(), ensure_ascii=False)}\n\n"

def errorTalkResponse(e):
    return f"data:{json.dumps({'error':str(e)}, ensure_ascii=False)}\n\n"