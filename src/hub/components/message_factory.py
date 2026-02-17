from ...config.config import Prompts
from ..entities import Message
    
def createSystemMessage() -> Message:
    return Message(role="system", content=Prompts["system_content"])

def createUserMessage(userInput) -> Message:
    return Message(role="user", content=userInput)

def createNewUserMessages(userInput) -> list:
    messages = []
    messages.append(createSystemMessage())
    messages.append(createUserMessage(userInput=userInput))
    return messages

def adaptMessages(messages) -> list:
    ms = []
    for m in messages:
        ms.append(m.__dict__)
    return ms