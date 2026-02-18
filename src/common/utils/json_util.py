import json

def toJson(dict: dict) -> str:
    return json.dumps(dict, ensure_ascii=False)

def fromJson(jsonStr: str) -> dict:
    return json.loads(jsonStr)