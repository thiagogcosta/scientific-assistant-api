from src.templates.singleton import Singleton


# RagAgent
class RagAgentBase(Singleton):
    def get_agent(self):
        raise NotImplementedError

    def retrieve():
        raise NotImplementedError

    def generation(self):
        raise NotImplementedError

    def structured_generation(self):
        raise NotImplementedError
