import dashscope
from src.config.config import envConfig

def call(model, messages, tools, enableThinking):
    kwargs = {
        'api_key': envConfig.get('DASHSCOPE_API_KEY'),
        'model': model,
        'messages': messages,
        'tools': tools,
        'enable_thinking': enableThinking,
        'result_format': 'message',
        'stream': True,
        'incremental_output': False,
        'parallel_tool_calls': True
    }
    return dashscope.Generation.call(**kwargs)