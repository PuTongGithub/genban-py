import dashscope
import os

def call(model, messages):
    return dashscope.Generation.call(
        api_key=os.getenv('DASHSCOPE_API_KEY'),
        model=model,
        messages=messages,
        result_format='message',
        stream=True,
        incremental_output=True
    )