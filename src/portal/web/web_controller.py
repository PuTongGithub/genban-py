import traceback
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from ...config.config import AppConfig
from .web_entitys import *
from ...kernel.core.core import genban_core

router = APIRouter(prefix="/api", tags=["web api"])

@router.get("/get_models")
def getModels():
    return AppConfig["hub"]["model_list"]

@router.get("/new_session")
def newSession() -> str:
    return genban_core.newSession()

@router.post("/talk")
async def talk(request: TalkRequest) -> StreamingResponse:
    def web_talk():
        try:
            res = genban_core.talk(sessionId=request.sessionId, userInput=request.userInput, model=request.model)
            for r in res:
                yield adaptTalkResponse(r)
        except Exception as e:
            traceback.print_exc()
            yield errorTalkResponse(e)
    return StreamingResponse(
        web_talk(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )
