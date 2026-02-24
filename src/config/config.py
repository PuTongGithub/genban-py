import json
import os
from pathlib import Path
from dotenv import load_dotenv
from src.common.utils.path_util import get_app_dirs, get_user_dirs
from src.common.exceptions import EnvConfigNotFoundException

class EnvConfig:
    def __init__(self):
        load_dotenv()

    def get(self, key: str) -> str:
        str = os.getenv(key)
        if not str:
            raise EnvConfigNotFoundException(key)
        return str

class AppConfig:
    def __init__(self):
        app_config_path = Path(__file__).parent / "jsons/app_config.json"
        with open(app_config_path, "r", encoding="utf-8") as file:
            self.config = json.load(file)
            self._set_file_whitelist()
            self._init_configs()

    # 设置读写文件默认白名单
    def _set_file_whitelist(self) -> None:
        self.config["tools"]["read_file_path_whitelist"].extend(get_app_dirs())
        self.config["tools"]["read_file_path_whitelist"].extend(get_user_dirs())
        self.config["tools"]["write_file_path_whitelist"].extend(get_app_dirs())
        self.config["tools"]["write_file_path_whitelist"].extend(get_user_dirs())

    # 初始化默认模型
    def _init_configs(self) -> None:
        for key, value in self.config["models"].items():
            if value.get("default", False):
                self.default_model = key
                break

    def get(self, key: str):
        return self.config.get(key)
    
    def getDefaultModel(self) -> str:
        return self.default_model

    def getModelConfig(self, model: str) -> dict:
        return self.config["models"].get(model)

class Prompts:
    def __init__(self):
        prompts_path = Path(__file__).parent / "jsons/prompts.json"
        with open(prompts_path, "r", encoding="utf-8") as file:
            self.config = json.load(file)
    
    def get(self, key: str) -> str:
        return self.config.get(key)
    
env_config = EnvConfig()
app_config = AppConfig()
prompts = Prompts()