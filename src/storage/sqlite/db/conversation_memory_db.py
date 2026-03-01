from typing import Optional, List
from ..database import db_execute, db_query
from ..models import ConversationMemory
from src.common.utils import time_util


class _ConversationMemoryDb:
    # 对话记忆数据访问层

    @db_execute
    def create(
        self,
        db,
        id: str,
        user_id: str,
        source: str,
        chat_id_start: str,
        chat_id_end: str,
        start_time: int,
        end_time: int,
        content: str
    ) -> bool:
        # 创建对话记忆
        try:
            memory = ConversationMemory(
                id=id,
                user_id=user_id,
                source=source,
                chat_id_start=chat_id_start,
                chat_id_end=chat_id_end,
                start_time=start_time,
                end_time=end_time,
                content=content,
                created_at=time_util.getTimestamp()
            )
            db.add(memory)
            return True
        except Exception:
            return False

    @db_query
    def get_by_id(self, db, id: str) -> Optional[ConversationMemory]:
        # 根据 id 查询对话记忆
        return db.query(ConversationMemory).filter(ConversationMemory.id == id).first()

    @db_query
    def get_by_time_range(
        self,
        db,
        user_id: str,
        start_time: int,
        end_time: int,
        limit: int = 100
    ) -> List[ConversationMemory]:
        # 根据时间范围查询对话记忆列表
        return db.query(ConversationMemory).filter(
            ConversationMemory.user_id == user_id,
            ConversationMemory.start_time >= start_time,
            ConversationMemory.end_time <= end_time
        ).order_by(ConversationMemory.created_at.desc()).limit(limit).all()

conversationMemoryDb = _ConversationMemoryDb()
