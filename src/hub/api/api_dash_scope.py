import dashscope
from src.config.config import getEnvConfig

def call(model, messages, tools):
    return dashscope.Generation.call(
        api_key=getEnvConfig('DASHSCOPE_API_KEY'),
        model=model,
        messages=messages,
        tools=tools,
        result_format='message',
        stream=True,
        incremental_output=False
    )