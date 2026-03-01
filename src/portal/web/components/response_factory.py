import re
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

def _cleanContent(content: str) -> str:
    # 移除开头的 [] 包裹内容
    if content:
        return re.sub(r'^\[[^\]]*\]', '', content)
    return content

def adaptTalkResponse(chat : Chat):
    res = TalkResponse()
    res.type = chat.type
    res.id = chat.id
    res.role = chat.message.role
    res.content = _cleanContent(chat.message.content)
    res.reasoning_content = chat.message.reasoning_content
    res.tool_calls = chat.message.tool_calls
    return res.model_dump_json()
