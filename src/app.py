from fastapi import FastAPI
from .portal.web import web_controller

app = FastAPI()
app.include_router(web_controller.router)