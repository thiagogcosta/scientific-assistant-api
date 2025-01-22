from src.templates.singleton import Singleton


# LlamafileServerBase
class LlamafileServerBase(Singleton):
    def connect(self):
        raise NotImplementedError
