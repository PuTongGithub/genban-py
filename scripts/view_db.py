#!/usr/bin/env python3
"""
查看数据库表数据脚本
用法: python scripts/view_db.py [表名]
       python scripts/view_db.py              # 查看所有表
       python scripts/view_db.py users        # 查看用户表
       python scripts/view_db.py user_states  # 查看用户状态表
"""
import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.storage.sqlite.database import engine
from src.storage.sqlite.models import User, UserState
from sqlalchemy import inspect
from src.storage.sqlite.database import SessionLocal


def get_tables():
    # 获取所有表名
    inspector = inspect(engine)
    return inspector.get_table_names()


def view_users():
    # 查看用户表
    db = SessionLocal()
    try:
        users = db.query(User).all()
        print("\n=== 用户表 (users) ===")
        print(f"{'user_id':<20} {'password_hash':<50} {'created_at':<15}")
        print("-" * 90)
        for user in users:
            print(f"{user.user_id:<20} {user.password_hash:<50} {user.created_at:<15}")
        print(f"\n共 {len(users)} 条记录")
    finally:
        db.close()


def view_user_states():
    # 查看用户状态表
    from src.storage.database import SessionLocal
    db = SessionLocal()
    try:
        states = db.query(UserState).all()
        print("\n=== 用户状态表 (user_states) ===")
        print(f"{'user_id':<20} {'deep_thinking':<15} {'model':<25} {'token_expires_at':<18} {'updated_at':<15}")
        print("-" * 100)
        for state in states:
            token_status = "有" if state.token else "无"
            expires = state.token_expires_at if state.token_expires_at else "-"
            print(f"{state.user_id:<20} {str(state.deep_thinking):<15} {state.model:<25} {str(expires):<18} {state.updated_at:<15}")
        print(f"\n共 {len(states)} 条记录")
    finally:
        db.close()


def view_all():
    # 查看所有表
    tables = get_tables()
    print(f"数据库表: {', '.join(tables)}")
    
    if 'users' in tables:
        view_users()
    if 'user_states' in tables:
        view_user_states()


def main():
    if len(sys.argv) < 2:
        view_all()
    else:
        table_name = sys.argv[1].lower()
        if table_name == 'users':
            view_users()
        elif table_name in ['user_states', 'userstates']:
            view_user_states()
        else:
            print(f"未知表名: {table_name}")
            print("可用表: users, user_states")


if __name__ == "__main__":
    main()
