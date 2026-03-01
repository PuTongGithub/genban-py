from .prompts.steward_prompt import STEWARD_PROMPT

class _PromptsLoader:
    
    def getStewardPrompt(self) -> str:
        return STEWARD_PROMPT

promptsLoader = _PromptsLoader()