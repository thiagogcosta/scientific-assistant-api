import os

from src.templates.singleton import Singleton


class Config(Singleton):
    def __init__(self):
        self.chroma_host = os.environ.get('CHROMA_HOST', '')
        self.chroma_port = os.environ.get('CHROMA_PORT', '')
        self.chroma_client_auth_provider = os.environ.get(
            'CHROMA_SERVER_AUTHN_PROVIDER', ''
        )
        self.chroma_client_auth_credentials = os.environ.get(
            'CHROMA_SERVER_AUTHN_CREDENTIALS', ''
        )
        self.chroma_auth_token_transport_header = os.environ.get(
            'CHROMA_AUTH_TOKEN_TRANSPORT_HEADER', ''
        )
        self.chroma_collection = os.environ.get('CHROMA_COLLECTION', '')
        self.embedding_model_name = os.environ.get('EMBEDDING_MODEL_NAME', '')
        self.web_server_link = os.environ.get('WEB_SERVER_LINK', '')
        self.web_server_key = os.environ.get('WEB_SERVER_KEY', '')
        self.rag_n_predict = os.environ.get('RAG_N_PREDICT', '')
        self.rag_temperature = os.environ.get('RAG_TEMPERATURE', '')
        self.api_key = os.environ.get('API_KEY', '')
