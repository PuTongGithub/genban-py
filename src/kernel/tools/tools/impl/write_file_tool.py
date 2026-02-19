from ..tool import Tool
from pathlib import Path
from src.config.config import AppConfig
from src.common.utils.path_util import validate_path

class WriteFileTool(Tool):

    @property
    def name(self) -> str:
        return "write_file"

    @property
    def description(self) -> str:
        return "创建一个新文件并写入内容，或向一个已存在文件内写入并覆盖原有内容"

    @property
    def parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "要写入的文件路径"
                },
                "content": {
                    "type": "string",
                    "description": "要写入的内容"
                }
            },
            "required": ["file_path", "content"]
        }

    def call(self, arguments: dict) -> str:
        file_path = arguments["file_path"]
        content = arguments["content"]
        if not validate_path(file_path, AppConfig["tools"]["write_file_path_whitelist"]):
            return "文件路径不在白名单内"
        try:
            Path(file_path).write_text(content, encoding="utf-8")
            return f"成功写入文件 {file_path}"
        except Exception as e:
            return f"写入文件 {file_path} 时出错: {e}"