import tomllib
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

def getEnvConfig(key: str) -> str:
    return os.getenv(key)

app_config_path = Path(__file__).parent / "tomls/app_config.toml"
with open(app_config_path, "rb") as file:
    AppConfig = tomllib.load(file)

prompts_path = Path(__file__).parent / "tomls/prompts.toml"
with open(prompts_path, "rb") as file:
    Prompts = tomllib.load(file)