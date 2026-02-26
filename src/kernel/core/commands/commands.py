from src.config.config import appConfig
from src.common.exceptions import ModelNotFoundException
from src.storage.sqlite.models import UserState

# 指令定义：键为指令前缀，值为处理类型
_COMMANDS = {
    "/openthink": "open_think",
    "/开启思考": "open_think",
    "/closethink": "close_think",
    "/关闭思考": "close_think",
    "/status": "status",
    "/状态": "status",
    "/model:": "model",
    "/模型:": "model",
    "/模型：": "model",
}

# 逐个处理用户输入中包含的指令，返回处理结果字符串列表以及去掉指令的用户输入
def handleCommand(state: UserState, userInput: str) -> tuple[list[str], str, bool]:
    commandResults = []
    stateChanged = False
    while True:
        userInput = userInput.strip()
        matched = False
        for prefix, cmdType in _COMMANDS.items():
            if userInput.startswith(prefix):
                matched = True
                remaining = userInput[len(prefix):]
                
                if cmdType == "open_think":
                    state.deep_thinking = True
                    userInput = remaining
                    stateChanged = True
                elif cmdType == "close_think":
                    state.deep_thinking = False
                    userInput = remaining
                    stateChanged = True
                elif cmdType == "status":
                    commandResults.append(_handleStatus(state))
                    userInput = remaining
                elif cmdType == "model":
                    parts = remaining.split(None, 1)
                    modelName = parts[0] if parts else ""
                    _handleModelSwitch(state, modelName)
                    userInput = remaining[len(modelName):]
                    stateChanged = True
                break
        
        if not matched:
            break
    
    return commandResults, userInput.strip(), stateChanged

def _handleModelSwitch(state: UserState, modelName: str):
    modelName = modelName.strip()
    if appConfig.getModelConfig(modelName) is None:
        raise ModelNotFoundException(modelName)
    state.model = modelName

def _handleStatus(state: UserState) -> str:
    deepThinkingStatus = "开启" if state.deep_thinking else "关闭"
    result = f"当前配置：\n- 模型：{state.model}\n- 深度思考：{deepThinkingStatus}"
    return result
