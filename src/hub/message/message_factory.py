from ...config.config import Prompts
from .message import Message
    
def createSystemMessage():
    systemMessage = Message("system", Prompts["system_content"])
    return systemMessage

def createUserMessage(userInput):
    userMessage = Message("user", userInput)
    return userMessage

def createNewUserMessages(userInput):
    messages = []
    messages.append(createSystemMessage())
    messages.append(createUserMessage(userInput=userInput))
    return messages

def adaptMessages(messages):
    ms = []
    for m in messages:
        ms.append(m.__dict__)
    return ms