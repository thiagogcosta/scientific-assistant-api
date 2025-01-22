from llama_cpp_agent.providers import LlamaCppServerProvider

from src.connections.config import Config
from src.templates.llamafile_server_base import LlamafileServerBase


# LlamafileServer
class LlamafileServer(LlamafileServerBase):
    def connect(self, *, config: Config) -> LlamaCppServerProvider:
        return LlamaCppServerProvider(
            server_address=config.web_server_link, api_key=config.web_server_key
        )

    def get_settings(self, *, config: Config, provider: LlamaCppServerProvider):
        settings = provider.get_provider_default_settings()
        settings.n_predict = int(config.rag_n_predict)
        settings.temperature = float(config.rag_temperature)

        return settings
