from ..tool import Tool
from pathlib import Path
from src.config.config import AppConfig
from src.common.utils.path_util import validate_path
from src.common.utils.json_util import toJson

class ReadFileTool(Tool):
    
    @property
    def name(self) -> str:
        return "read_file"

    @property
    def description(self) -> str:
        return "读取文件内容，返回文件所有行内容的JSON数组"

    @property
    def parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "文件路径"
                }
            },
            "required": ["file_path"]
        }

    def call(self, arguments: dict) -> str:
        file_path = arguments["file_path"]
        if not validate_path(file_path, AppConfig["tools"]["read_file_path_whitelist"]):
            return "文件路径不在白名单内"
        path = Path(file_path)
        # 读取所有行（保留原始换行符）
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        return toJson(lines)