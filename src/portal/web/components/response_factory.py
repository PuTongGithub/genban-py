from src.common.entities import Chat
from src.portal.web.entitys import TalkResponse
from src.common.utils.json_util import toJson

def buildSSEContent(event : str, message : str) -> str:
    return f"event: {event}\ndata: {message}\n\n"

def buildErrorSSEContent(error) -> str:
    return buildSSEContent(event="error", message=toJson({'error':str(error)}))

def buildCompleteSSEContent() -> str:
    return buildSSEContent(event="complete", message="")

def buildChatSSEContent(chat : Chat) -> str:
    return buildSSEContent(event="message", message=adaptTalkResponse(chat))

def adaptTalkResponse(chat : Chat):
    res = TalkResponse()
    res.role = chat.message.role
    res.content = chat.message.content
    res.reasoning_content = chat.message.reasoning_content
    return res.model_dump_json()
