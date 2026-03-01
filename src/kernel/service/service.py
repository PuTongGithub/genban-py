from ..conversation.conversation_holder import conversationHolder
from src.user.user_manager import userManager
import asyncio

# 服务类，负责对接用户输入和输出
class _Service:

    # 向对话管理器提交用户输入，返回本条用户输入的 id
    async def submitUserInput(self, userId, userInput) -> str:
        conversationHandler = conversationHolder.getConversationHandler(userId)
        return conversationHandler.submitUserInput(userInput)
    
    # 订阅 SSE 推送
    def subscribeStream(self, userId) -> asyncio.Queue:
        conversationHandler = conversationHolder.getConversationHandler(userId)
        return conversationHandler.subscribe()
    
    # 取消订阅
    def unsubscribeStream(self, userId, queue: asyncio.Queue):
        conversationHandler = conversationHolder.getConversationHandler(userId)
        conversationHandler.unsubscribe(queue)

service = _Service()
