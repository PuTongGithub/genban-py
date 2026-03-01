import traceback
from fastapi import APIRouter, Header, HTTPException
from fastapi.responses import StreamingResponse
from .entitys import *
from src.kernel.service.service import service
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

@router.post("/submit")
async def submit(
    request: SubmitRequest,
    authorization: str = Header(None)
) -> SubmitResponse:
    try:
        token = extractToken(authorization)
        userId = userManager.validateToken(token)
    except UnauthorizedException:
        raise HTTPException(status_code=401, detail="Unauthorized")

    chatId = await service.submitUserInput(userId, request.user_input)
    return SubmitResponse(chat_id=chatId)

@router.post("/stream")
async def stream(
    authorization: str = Header(None)
):
    # SSE 流式对话接口
    try:
        token = extractToken(authorization)
        userId = userManager.validateToken(token)
    except UnauthorizedException:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    # 订阅推送
    queue = service.subscribeStream(userId)
    
    # 创建 SSE 流生成器
    async def generate():
        try:
            # 持续接收推送直到完成
            while True:
                # 等待新消息，超时 1 秒用于检查连接状态
                chat = await queue.get()
                yield response_factory.buildChatSSEContent(chat)
        except Exception as e:
            yield response_factory.buildErrorSSEContent(e)
        finally:
            # 取消订阅
            service.unsubscribeStream(userId, queue)
            yield response_factory.buildCompleteSSEContent()
    
    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )
