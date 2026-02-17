from .api import api_dash_scope
from .components import api_formatter, message_factory
from src.common.entities import Chat

class _AiHub:

    def __init__(self):
        pass

    def _buildMessages(self, messages, userInput):
        if len(messages) == 0:
            ms = message_factory.createNewUserMessages(userInput)
            for m in ms:
                messages.append(m)
        else:
            messages.append(message_factory.createUserMessage(userInput))
        return message_factory.adaptMessages(messages)

    # 调用大模型接口，返回结果非增量型流式输出（即最后一次流式输出结果为完整结果）
    def chat(self, oldMessages, userInput, model) -> Chat:
        messages = self._buildMessages(messages=oldMessages, userInput=userInput)
        responses = api_dash_scope.call(model=model, messages=messages)
        for r in responses:
            m = api_formatter.dashScopeResponseFormat(r)
            yield m
        
ai_hub = _AiHub()