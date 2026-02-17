import dashscope
from src.config.config import getEnvConfig

def call(model, messages):
    return dashscope.Generation.call(
        api_key=getEnvConfig('DASHSCOPE_API_KEY'),
        model=model,
        messages=messages,
        result_format='message',
        stream=True,
        incremental_output=False
    )