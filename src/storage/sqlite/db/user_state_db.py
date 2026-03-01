from typing import Optional
from ..database import db_execute, db_query
from ..models import UserState
from src.common.utils import time_util


class _UserStateDb:
    # 用户状态数据访问层

    @db_execute
    def create(self, db, user_id: str, deep_thinking: bool, model: str) -> bool:
        # 创建用户状态
        try:
            state = UserState(
                user_id=user_id,
                deep_thinking=deep_thinking,
                model=model,
                updated_at=time_util.getTimestamp(),
                current_chat_id=""
            )
            db.add(state)
            return True
        except Exception:
            return False

    @db_execute
    def update(self, db, state: UserState) -> bool:
        # 更新用户状态
        existing = db.query(UserState).filter(UserState.user_id == state.user_id).first()
        if existing:
            existing.deep_thinking = state.deep_thinking
            existing.model = state.model
            existing.updated_at = time_util.getTimestamp()
            existing.token = state.token
            existing.token_expires_at = state.token_expires_at
            return True
        return False

    @db_query
    def get_by_user_id(self, db, user_id: str) -> Optional[UserState]:
        # 根据 user_id 查询用户状态
        return db.query(UserState).filter(UserState.user_id == user_id).first()

    @db_query
    def get_by_token(self, db, token: str) -> Optional[UserState]:
        # 根据 token 查询用户状态
        return db.query(UserState).filter(UserState.token == token).first()


userStateDb = _UserStateDb()
