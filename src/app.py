from fastapi import FastAPI
from .portal.web import controller

app = FastAPI()
app.include_router(controller.router)