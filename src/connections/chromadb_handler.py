import chromadb
from chromadb.config import Settings
from rag.utils import get_embedding_function

from src.connections.config import Config
from src.templates.chromadb_base import ChromaDBBase


# ChromaDB
class ChromaDBHandler(ChromaDBBase):
    def connect(self, *, config: Config) -> chromadb.HttpClient:
        host = f'http://{config.chroma_host}:{config.chroma_port}'

        client = chromadb.HttpClient(
            host=host,
            settings=Settings(
                allow_reset=True,
                anonymized_telemetry=False,
                chroma_client_auth_provider=config.chroma_client_auth_provider,
                chroma_client_auth_credentials=config.chroma_client_auth_credentials,
                chroma_auth_token_transport_header=config.chroma_auth_token_transport_header,
            ),
        )

        return client

    def get_collection(self, *, client: chromadb.HttpClient, config: Config):
        return client.get_collection(
            name=config.chroma_collection,
            embedding_function=get_embedding_function(
                embedding_model_name=config.embedding_model_name
            ),
        )
