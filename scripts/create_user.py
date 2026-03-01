#!/usr/bin/env python3
"""
创建用户脚本
用法: python scripts/create_user.py
"""
import sys
import getpass
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.config.config import appConfig
from src.storage.sqlite.db.user_db import userDb
from src.storage.sqlite.db.user_state_db import userStateDb
from src.user.components.password_util import hashPassword


def create_user():
    print("=== 创建用户 ===\n")

    # 输入用户ID
    user_id = input("请输入用户ID: ").strip()
    if not user_id:
        print("错误: 用户ID不能为空")
        return

    # 检查用户是否已存在
    existing_user = userDb.get_user_by_id(user_id)
    if existing_user:
        print(f"错误: 用户 {user_id} 已存在")
        return

    # 输入密码
    password = getpass.getpass("请输入密码: ")
    if len(password) < 6:
        print("错误: 密码最少需要6位字符")
        return

    # 确认密码
    confirm_password = getpass.getpass("确认密码: ")
    if password != confirm_password:
        print("错误: 两次输入的密码不一致")
        return

    # 创建用户
    password_hash = hashPassword(password)
    success = userDb.create_user(user_id, password_hash)

    if not success:
        print(f"\n✗ 用户创建失败")
        return

    # 初始化用户状态
    default_model = appConfig.getDefaultModel()
    state_success = userStateDb.create(user_id, False, default_model)

    if state_success:
        print(f"\n✓ 用户 {user_id} 创建成功！")
    else:
        print(f"\n⚠ 用户创建成功，但状态初始化失败")


if __name__ == "__main__":
    create_user()
