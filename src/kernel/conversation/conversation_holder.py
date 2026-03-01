from .conversation_handler import ConversationHandler

# 对话管理器
class _ConversationHolder:

    def __init__(self):
        self.conversationHandlerMap = {}
    
    # 获取用户对话对象
    def getConversationHandler(self, userId: str) -> ConversationHandler:
        if userId not in self.conversationHandlerMap:
            self.conversationHandlerMap[userId] = ConversationHandler(userId)

        return self.conversationHandlerMap[userId]

conversationHolder = _ConversationHolder()
