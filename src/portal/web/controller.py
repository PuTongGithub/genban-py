import traceback
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from src.config.config import AppConfig
from .entitys import *
from src.kernel.core.core import genban_core
from .components import response_factory

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
            res = genban_core.talk(sessionId=request.session_id, userInput=request.user_input, model=request.model)
            for r in res:
                yield response_factory.buildChatSSEContent(r)
            yield response_factory.buildCompleteSSEContent()
        except Exception as e:
            traceback.print_exc()
            yield response_factory.buildErrorSSEContent(e)
    return StreamingResponse(
        web_talk(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )
