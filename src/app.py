import atexit
from fastapi import FastAPI
from contextlib import asynccontextmanager
from .portal.web import controller
from .common.async_executor import AsyncExecutor

atexit.register(AsyncExecutor.stop_all)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 应用启动
    yield
    # 应用关闭：优雅停机，停止所有 AsyncExecutor
    AsyncExecutor.stop_all()

app = FastAPI(lifespan=lifespan)
app.include_router(controller.router)