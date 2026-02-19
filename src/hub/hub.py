from .api import api_dash_scope
from .components import api_formatter
from src.common.entities import CallResponse
from src.common.exceptions import CallHubException

class _AiHub:

    def __init__(self):
        pass

    # 调用大模型接口，返回结果非增量型流式输出（即最后一次流式输出结果为完整结果）
    def call(self, messages, model, tools) -> CallResponse:
        responses = api_dash_scope.call(model=model, messages=messages, tools=tools)
        for r in responses:
            if r.status_code != 200:
                raise CallHubException(str(r))
            m = api_formatter.dashScopeResponseFormat(r)
            yield m
        
ai_hub = _AiHub()