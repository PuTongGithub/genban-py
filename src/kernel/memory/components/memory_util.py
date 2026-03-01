from pathlib import Path

from src.common.entities import Chat, Message
from src.common.utils.path_util import get_data_dir
from src.common.utils import time_util


def getDateFromTimestamp(timestamp: int) -> str:
    # 从时间戳获取日期字符串 YYYYMMDD
    return time_util.timestampToStr(timestamp, time_util.STR_FORMATTER_DATE_NO_MARKS)


def getChatDir(userId: str) -> Path:
    # 获取用户 chat 存储目录
    return get_data_dir() / "memory" / userId / "chat"


def getChatFilePath(userId: str, date: str) -> Path:
    # 获取指定日期的 chat 文件路径
    return getChatDir(userId) / f"{date}.jsonl"


def dictToChat(data: dict) -> Chat:
    # 字典转 Chat 对象
    chat = Chat()
    chat.type = data.get("type", "")
    chat.id = data.get("id", "")
    chat.override_id_begin = data.get("override_id_begin")
    chat.override_id_end = data.get("override_id_end")
    chat.time = data.get("time", 0)
    chat.total_tokens = data.get("total_tokens", 0)

    messageData = data.get("message")
    if messageData:
        chat.message = Message(
            role=messageData.get("role", ""),
            content=messageData.get("content", ""),
            reasoning_content=messageData.get("reasoning_content", ""),
            tool_calls=messageData.get("tool_calls"),
            tool_call_id=messageData.get("tool_call_id")
        )

    return chat
