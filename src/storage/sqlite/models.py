from typing import Optional
from sqlalchemy import String, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from .database import Base, engine

# 用户模型
class User(Base):
    __tablename__ = "users"

    user_id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[int] = mapped_column(Integer, nullable=False)

# 用户状态模型
class UserState(Base):
    __tablename__ = "user_states"

    user_id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    deep_thinking: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    model: Mapped[str] = mapped_column(String, nullable=False)
    updated_at: Mapped[int] = mapped_column(Integer, nullable=False)
    token: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    token_expires_at: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

# 对话记忆模型
class ConversationMemory(Base):
    __tablename__ = "conversation_memories"

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    user_id: Mapped[str] = mapped_column(String, nullable=False, index=True)
    source: Mapped[str] = mapped_column(String, nullable=False)
    chat_id_start: Mapped[str] = mapped_column(String, nullable=False)
    chat_id_end: Mapped[str] = mapped_column(String, nullable=False)
    start_time: Mapped[int] = mapped_column(Integer, nullable=False)
    end_time: Mapped[int] = mapped_column(Integer, nullable=False)
    content: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[int] = mapped_column(Integer, nullable=False)

# 创建表
Base.metadata.create_all(bind=engine)
