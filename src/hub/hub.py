from .api import api_dash_scope
from .components import api_formatter
from src.common.entities import CallResponse
from src.common.exceptions import CallHubException, ModelNotFoundException
from src.config.config import app_config

class _AiHub:

    def __init__(self):
        pass

    def call(self, messages, model, tools, enableThinking) -> CallResponse:
        modelConfig = app_config.getModelConfig(model)
        if modelConfig is None:
            raise ModelNotFoundException(model)
        responses = api_dash_scope.call(model=modelConfig["id"], messages=messages, tools=tools, enableThinking=enableThinking) 
        for r in responses:
            if r.status_code != 200:
                raise CallHubException(str(r))
            m = api_formatter.dashScopeResponseFormat(r)
            yield m
        
ai_hub = _AiHub()