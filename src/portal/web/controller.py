import traceback
from fastapi import APIRouter, Header, HTTPException
from fastapi.responses import StreamingResponse
from .entitys import *
from src.kernel.core.core import genbanCore
from src.user.user_manager import userManager
from src.common.exceptions import UserNotFoundException, InvalidPasswordException, UnauthorizedException
from .components import response_factory

router = APIRouter(prefix="/api", tags=["web api"])


def extractToken(authorization: str) -> str:
    # 从 Authorization header 提取 token
    if not authorization or not authorization.startswith("Bearer "):
        raise UnauthorizedException()
    return authorization[7:]


@router.post("/login")
async def login(request: LoginRequest) -> LoginResponse:
    # 用户登录接口
    try:
        state = userManager.login(request.user_id, request.password)
        return LoginResponse(
            token=state.token,
            expires_at=state.token_expires_at
        )
    except UserNotFoundException:
        return LoginResponse(error="User not found")
    except InvalidPasswordException:
        return LoginResponse(error="Invalid password")
    except Exception as e:
        traceback.print_exc()
        return LoginResponse(error=str(e))


@router.post("/talk")
async def talk(
    request: TalkRequest,
    authorization: str = Header(None)
) -> StreamingResponse:
    # 对话接口，需要携带 Authorization header
    try:
        token = extractToken(authorization)
        userId = userManager.validateToken(token)
    except UnauthorizedException:
        raise HTTPException(status_code=401, detail="Unauthorized")

    def web_talk():
        try:
            res = genbanCore.talk(userId=userId, userInput=request.user_input)
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
