from .api import api_dash_scope
from .components import api_formatter
from src.common.exceptions import CallHubException, ModelNotFoundException
from src.config.config import appConfig

class _AiHub:

    def call(self, messages, model, tools, enableThinking):
        modelConfig = appConfig.getModelConfig(model)
        if modelConfig is None:
            raise ModelNotFoundException(model)
        response = api_dash_scope.call(
            model=modelConfig["id"], 
            messages=messages, 
            tools=tools, 
            enableThinking=enableThinking
        )
        
        if response.status_code != 200:
            raise CallHubException(str(response))
        return api_formatter.dashScopeResponseFormat(response)
        
aiHub = _AiHub()