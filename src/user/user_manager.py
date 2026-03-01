import secrets

from src.common.exceptions import UserNotFoundException, InvalidPasswordException, UnauthorizedException
from src.common.utils import time_util
from src.storage.sqlite.models import UserState
from src.storage.sqlite.db.user_db import userDb
from src.storage.sqlite.db.user_state_db import userStateDb
from .components.password_util import verifyPassword

class _UserManager:
    # 用户管理器 - 状态管理和认证

    TOKEN_EXPIRE_SECONDS = 7 * time_util.ONE_DAY_SECOND  # 7天

    def getState(self, userid: str) -> UserState:
        # 获取用户状态
        state = userStateDb.get_by_user_id(userid)
        if state is None:
            raise UserNotFoundException(userid)
        return state

    def updateState(self, state: UserState) -> bool:
        # 更新用户状态
        return userStateDb.update(state)

    def login(self, userId: str, password: str) -> UserState:
        # 登录，成功返回用户状态
        user = userDb.get_user_by_id(userId)
        if user is None:
            raise UserNotFoundException(userId)

        if not verifyPassword(password, user.password_hash):
            raise InvalidPasswordException()

        state = userStateDb.get_by_user_id(userId)
        if state is None:
            raise UserNotFoundException(userId)

        # 创建 token
        state.token = secrets.token_urlsafe(32)
        state.token_expires_at = time_util.getTimestamp() + self.TOKEN_EXPIRE_SECONDS

        # 持久化到数据库
        userStateDb.update(state)

        return state

    def validateToken(self, token: str) -> str:
        # 校验 token，返回 user_id
        state = userStateDb.get_by_token(token)
        if state is None:
            raise UnauthorizedException()

        if state.token_expires_at < time_util.getTimestamp():
            # token 过期
            raise UnauthorizedException()

        return state.user_id

userManager = _UserManager()
