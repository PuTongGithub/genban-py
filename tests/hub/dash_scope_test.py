from src.hub.api import api_dash_scope as ADS
from dotenv import load_dotenv

load_dotenv()

model_list = ["qwen3-14b", "qwen3-32b", "qwen3-max", "qwen-plus", "qwen-turbo"]
model="qwen3-14b"

messages = [
    {'role':'system','content':'你是一个聊天助手，说话风格简洁而简短。'},
    {'role': 'user','content': '四个直辖市今天的天气怎么样？'}
]

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "当你想查询指定城市的天气时非常有用。",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "城市或县区，比如北京市、杭州市、余杭区等。",
                    }
                },
                "required": ["location"],
            },
        },
    }
]

responses = ADS.call(model=model, messages=messages, tools=tools)

for r in responses:
    print("------")
    try:
        print(r.output.choices[0])
    except:
        print(r)
