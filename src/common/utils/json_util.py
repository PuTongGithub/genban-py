import json

def toJson(obj) -> str:
    return json.dumps(obj.__dict__, ensure_ascii=False)