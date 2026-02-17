from src.hub.api import api_dash_scope as ADS
from dotenv import load_dotenv

load_dotenv()

model="qwen3-14b"
messages = [
    {'role':'system','content':'你是一个聊天助手，说话风格简洁而简短。'},
    {'role': 'user','content': '你是谁？'}
]

responses = ADS.call(model=model, messages=messages)

for r in responses:
    print("------")
    cs = r.output.choices
    for c in cs:
        print(c.message)
        print(r.usage)
