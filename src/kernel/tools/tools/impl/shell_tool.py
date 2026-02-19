from ..tool import Tool
import subprocess
from src.common.utils import sys_util
from src.config.config import AppConfig

# 命令行执行工具
class ShellTool(Tool):

    @property
    def name(self) -> str:
        return "shell"

    @property
    def description(self) -> str:
        if sys_util.is_mswindows():
            sysTypeDesc ="当前系统是Windows"
        else:
            sysTypeDesc ="当前系统是Linux"
        return sysTypeDesc + "，使用该工具可以执行shell命令。在调用工具前请务必确保命令是安全的，避免执行恶意代码。"

    @property
    def parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "description": "要执行的shell命令"
                },
                "cwd": {
                    "type": "string",
                    "description": "命令执行的工作目录"
                }
            },
            "required": ["command"]
        }

    def call(self, arguments: dict) -> str:
        command = arguments["command"]
        cwd = arguments.get("cwd", None)
        timeout = AppConfig["tools"]["shell_timeout"]
        try:
            result = subprocess.run(
                command, 
                shell=True, 
                cwd=cwd, 
                check=True, 
                text=True, 
                capture_output=True,
                timeout=timeout
            )
            return result.stdout
        except subprocess.TimeoutExpired as e:
            return f"命令执行超时，超时时间：{timeout}秒\n标准输出：{e.stdout}\n标准错误：{e.stderr}"
        except subprocess.CalledProcessError as e:
            return f"命令执行失败，返回码：{e.returncode}\n标准输出：{e.stdout}\n标准错误：{e.stderr}"
