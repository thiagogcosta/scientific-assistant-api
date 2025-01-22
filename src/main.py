import os

import logfire
import uvicorn
from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import RedirectResponse

from src.connections.chromadb_handler import ChromaDBHandler
from src.connections.config import Config
from src.connections.llamafile_server import LlamafileServer
from src.logger import Logger
from src.rag.dataclass import AboutCategory, AboutScience
from src.rag.prompt_generator import (
    PromptGeneratorDefault,
    PromptGeneratorFiltered,
)
from src.rag.rag_agent import RagAgent

# -----DESC: Logger-----
logger = Logger().get_logger()
# --------------------------

app = FastAPI()

# -----DESC: Logfire Config-----
logfire.configure(
    token=os.environ.get('LOGFIRE_PROJECT_TOKEN', ''),
    pydantic_plugin=logfire.PydanticPlugin(record='all'),
)
logfire.instrument_fastapi(app)
# ------------------------------


@app.post('/rag')
async def get_response(question: str, prompt_type: str, key: str = Header(...)):
    # ------------------------------
    # DESC: Get the config
    config = Config()
    # ------------------------------

    # ------------------------------
    # DESC: Token validation
    if key != config.api_key:
        logfire.exception('Bad Request - Invalid API token', status_code=400)
        raise HTTPException(status_code=400, detail='Bad Request - Invalid API token')
    # ------------------------------

    # ------------------------------
    # DESC: Input validation
    if question is None or prompt_type not in ['default', 'start', 'end', 'filtered']:
        logfire.exception('Bad Request -  Invalid Input', status_code=400)
        raise HTTPException(status_code=400, detail='Bad Request -  Invalid Input')
    # ------------------------------

    # ------------------------------
    # DESC: Connections

    # Llamafile Server
    llamafile_server = LlamafileServer()
    provider = llamafile_server.connect(config=config)

    settings = llamafile_server.get_settings(config=config, provider=provider)

    # ChromaDB
    chromadb_handler = ChromaDBHandler()
    chromadb_client = chromadb_handler.connect(config=config)

    collection = chromadb_handler.get_collection(client=chromadb_client, config=config)

    logger.info('-' * 50)
    logger.info(f'Quantidade de itens na coleção: {collection.count()}')
    logger.info('-' * 50)

    logfire.info('itens na coleção', quantidade=collection.count())

    # ------------------------------

    # DESC: RAG

    rag_agent = RagAgent()

    agent = rag_agent.get_agent(
        provider=provider, prompt=PromptGeneratorDefault().get_prompt()
    )

    if prompt_type == 'filtered':
        prompt = rag_agent.retrieve(
            user_input=question,
            collection=collection,
            prompt=PromptGeneratorFiltered().get_prompt(),
        )

        result = rag_agent.generation(
            agent=agent, settings=settings, user_input=question, prompt=prompt
        )

    elif prompt_type == 'start':
        result = rag_agent.structured_generation(
            provider=provider, dataclass=AboutScience, question=question
        )

    elif prompt_type == 'end':
        result = rag_agent.structured_generation(
            provider=provider, dataclass=AboutCategory, question=question
        )
    # ------------------------------

    return {'response': result}


@app.get('/', include_in_schema=False)
async def docs_redirect():
    return RedirectResponse(url='/docs')


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
