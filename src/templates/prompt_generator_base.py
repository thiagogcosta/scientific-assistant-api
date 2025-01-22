from src.templates.singleton import Singleton


# PromptGeneratorBase
class PromptGeneratorBase(Singleton):
    def get_prompt(self):
        raise NotImplementedError
