from sqlalchemy import Column, String, Integer, Boolean
from src.storage.database import Base, engine


class User(Base):
    # 用户模型
    __tablename__ = "users"

    user_id = Column(String, primary_key=True, index=True)
    password_hash = Column(String, nullable=False)
    created_at = Column(Integer, nullable=False)


class UserState(Base):
    # 用户状态模型
    __tablename__ = "user_states"

    user_id = Column(String, primary_key=True, index=True)
    deep_thinking = Column(Boolean, default=False, nullable=False)
    model = Column(String, nullable=False)
    updated_at = Column(Integer, nullable=False)
    token = Column(String, nullable=True)
    token_expires_at = Column(Integer, nullable=True)


# 创建表
Base.metadata.create_all(bind=engine)
