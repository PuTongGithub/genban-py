from src.common.utils import json_util
from src.common.exceptions import ToolNotExistException
from .tools.impl.shell_tool import ShellTool
from .tools.impl.read_file_tool import ReadFileTool
from .tools.impl.write_file_tool import WriteFileTool
from .tools.impl.edit_file_tool import EditFileTool

# 工具调用类，实现统一的工具调用接口
class ToolCaller:

    # 初始化工具调用类，注册所有工具
    def __init__(self):
        self.toolsMap = {}
        self.tools = []
        self._registerTool(ShellTool())
        self._registerTool(ReadFileTool())
        self._registerTool(WriteFileTool())
        self._registerTool(EditFileTool())

    # 注册工具类
    def _registerTool(self, tool: Tool):
        self.toolsMap[tool.name] = tool
        self.tools.append(tool.definition)

    # 获取所有注册的工具定义
    def getTools(self) -> list:
        return self.tools

    # 执行工具调用，返回调用结果
    def callTool(self, toolCall) -> str:
        function = toolCall['function']
        name = function['name']
        arguments = json_util.fromJson(function['arguments'])
        tool = self.toolsMap.get(name)
        if tool is None:
            raise ToolNotExistException(name)
        return tool.call(arguments)

tool_caller = ToolCaller()