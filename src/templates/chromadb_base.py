from src.templates.singleton import Singleton


# ChromaDB
class ChromaDBBase(Singleton):
    def connect(self):
        raise NotImplementedError

    def get_collection(self):
        raise NotImplementedError

    def get_embedding_function(self):
        raise NotImplementedError
