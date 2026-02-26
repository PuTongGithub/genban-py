from .conversation import Conversation
from .components.chat_factory import chatFactory

# 对话管理器
class _ConversationHolder:

    def __init__(self):
        # 存储用户对话对象的映射表
        self.conversationMap = {}
    
    # 获取用户对话对象
    def getConversation(self, userId: str, userInput: str) -> Conversation:
        if userId not in self.conversationMap:
            self.conversationMap[userId] = Conversation(userId)
        conversation = self.conversationMap[userId]

        # 构建用户输入消息列表
        inputChats = chatFactory.createUserInputChats(
            isNewUser=len(conversation.chats) == 0, 
            userInput=userInput
        )
        conversation.extend(inputChats)

        return conversation

conversationHolder = _ConversationHolder()
