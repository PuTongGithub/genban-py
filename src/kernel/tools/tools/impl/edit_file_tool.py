from ..tool import Tool
from pathlib import Path
from src.config.config import AppConfig
from src.common.utils.path_util import validate_path
import tempfile

class EditFileTool(Tool):

    @property
    def name(self) -> str:
        return "edit_file"
    
    @property
    def description(self) -> str:
        return "编辑文件内容，修改指定行的内容"

    @property
    def parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "要编辑的文件路径"
                },
                "line_begin": {
                    "type": "integer",
                    "description": "要删除的起始行号（包含），从 0 开始计数"
                },
                "line_end": {
                    "type": "integer",
                    "description": "要删除的结束行号（包含）"
                },
                "content": {
                    "type": "string",
                    "description": "写入到删除行范围的新内容"
                }
            },
            "required": ["file_path", "line_begin", "line_end", "content"]
        }

    def call(self, arguments: dict) -> str:
        file_path = arguments["file_path"]
        line_begin = arguments["line_begin"]
        line_end = arguments["line_end"]
        content = arguments["content"]

        # 校验文件路径
        if not validate_path(file_path, AppConfig["tools"]["write_file_path_whitelist"]):
            return "文件路径不在白名单内"

        # 读取所有行（保留原始换行符）
        path = Path(file_path)
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        total_lines = len(lines)
        # 允许 line_end 超出文件末尾（自动截断到最后一行）
        actual_end = min(line_end, total_lines - 1)
        # 构建新内容
        new_lines = []
        new_lines.extend(lines[:line_begin])
        if not content.endswith('\n'):
            content += '\n'
        # 将 content 拆分为行，并保留每行的换行符
        new_content_lines = content.splitlines(keepends=True)
        if new_content_lines:
            new_lines.extend(new_content_lines)
        
        # 保留后面的行 (actual_end, end]
        new_lines.extend(lines[actual_end + 1:])
        
        # 写入临时文件（同目录，保证原子替换）
        with tempfile.NamedTemporaryFile(
            mode='w',
            encoding='utf-8',
            delete=False,
            dir=path.parent,
            suffix='.tmp'
        ) as tmp:
            tmp.writelines(new_lines)
            tmp_path = Path(tmp.name)
        
        # 原子替换原文件
        tmp_path.replace(path)
        return f"编辑文件 {file_path} 成功，修改了 {line_end - line_begin + 1} 行"
