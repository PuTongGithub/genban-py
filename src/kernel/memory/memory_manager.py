from dataclasses import asdict
from typing import List, Optional
from collections import defaultdict

from src.storage.file_storage import fileStorage
from src.common.entities import Chat
from src.common.utils import time_util
from .components import memory_util

# 记忆管理器 存储与检索
class _MemoryManager:

    # 向文件系统追加 Chat 记录
    def appendChats(self, userId: str, chats: List[Chat]) -> None:
        if not chats:
            return

        dateGroups = defaultdict(list)
        for chat in chats:
            date = memory_util.getDateFromTimestamp(chat.time)
            dateGroups[date].append(asdict(chat))

        for date, records in dateGroups.items():
            filePath = memory_util.getChatFilePath(userId, date)
            fileStorage.appendToJsonl(filePath, records)

    # 从文件系统读取指定时间范围内的 Chat 记录, 默认读取24小时内的记录
    def getChats(self, userId: str, startTime: Optional[int] = None, endTime: Optional[int] = None) -> List[Chat]:
        if startTime is None:
            startTime = time_util.getYesterdayTimestamp()
        if endTime is None:
            endTime = time_util.getTimestamp()

        startDate = memory_util.getDateFromTimestamp(startTime)
        endDate = memory_util.getDateFromTimestamp(endTime)

        chatDir = memory_util.getChatDir(userId)
        files = fileStorage.listJsonlFiles(chatDir, startDate, endDate)

        results = []
        for filePath in files:
            records = fileStorage.readJsonl(filePath)
            for record in records:
                if startTime <= record["time"] <= endTime:
                    results.append(memory_util.dictToChat(record))

        results.sort(key=lambda c: c.time)
        return results


memoryManager = _MemoryManager()
