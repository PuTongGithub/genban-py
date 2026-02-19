import tomllib
import os
from pathlib import Path
from dotenv import load_dotenv
from src.common.utils.path_util import get_app_dirs, get_user_dirs

load_dotenv()

def getEnvConfig(key: str) -> str:
    return os.getenv(key)

prompts_path = Path(__file__).parent / "tomls/prompts.toml"
with open(prompts_path, "rb") as file:
    Prompts = tomllib.load(file)

# 设置读写文件默认白名单
def _set_file_whitelist() -> None:
    AppConfig["tools"]["read_file_path_whitelist"].extend(get_app_dirs())
    AppConfig["tools"]["read_file_path_whitelist"].extend(get_user_dirs())
    AppConfig["tools"]["write_file_path_whitelist"].extend(get_app_dirs())
    AppConfig["tools"]["write_file_path_whitelist"].extend(get_user_dirs())
    
app_config_path = Path(__file__).parent / "tomls/app_config.toml"
with open(app_config_path, "rb") as file:
    AppConfig = tomllib.load(file)
    _set_file_whitelist()

