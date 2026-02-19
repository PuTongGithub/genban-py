from abc import ABC, abstractmethod

# 工具接口类
class Tool(ABC):

    # 工具名称
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    # 工具描述，用于大模型理解工具作用，可包含工具的功能、参数、返回值等信息
    @property
    @abstractmethod
    def description(self) -> str:
        pass

    # 工具调用入参定义
    @property
    def parameters(self) -> dict:
        return {}

    # 工具定义
    @property
    def definition(self) -> dict:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters,
            }
        }

    # 工具调用
    @abstractmethod
    def call(self, arguments: dict) -> str:
        pass