from fastapi import FastAPI
from .portal import web_controller
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
app.include_router(web_controller.router)