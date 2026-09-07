# scientific-assistant-api
[![Version](https://img.shields.io/badge/version-1.0.2-gray)](https://github.com/thiagogcosta/scientific-assistant-api/releases)
[![Docker](https://img.shields.io/badge/Docker-808080?logo=docker&logoColor=2496ED)](https://hub.docker.com/r/thiagogcosta/scientific-assistant-api)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**scientific-assistant-api** é uma API de RAG (Retrieval-Augmented Generation) construída com [FastAPI](https://fastapi.tiangolo.com/) para responder dúvidas sobre artigos científicos em português do Brasil.

A API combina um servidor [llamafile](https://github.com/Mozilla-Ocho/llamafile) como provedor de LLM, o [ChromaDB](https://www.trychroma.com/) como armazenamento vetorial e o [sentence-transformers](https://www.sbert.net/) para geração de embeddings, tudo orquestrado pelo [llama-cpp-agent](https://github.com/olivierdehaene/llama-cpp-agent).

## Requirements

- Python `>=3.10,<=3.12`
- [Poetry](https://python-poetry.org/) `1.8.3`
- Docker (para execução em container)

### Dependências principais

- `fastapi` e `uvicorn` — framework web e servidor ASGI
- `chromadb` `0.6.1` — armazenamento e busca vetorial
- `llama-cpp-agent` `0.2.35` — integração com o servidor llamafile
- `sentence-transformers` `3.2.0` — geração de embeddings
- `logfire` — observabilidade e tracing

## Installation

### Local

```bash
make local-start
```

Ou manualmente:

```bash
python3 -m pip install -q poetry==1.8.3
poetry install --only main
python3 -m poetry run src/main.py
```

### Docker

```bash
make build
make start
```

O `Makefile` também oferece os alvos `end`, `clear` e `clear_all` para gerenciar o ciclo de vida do container.

## Usage

A API expõe um único endpoint `POST /rag`, protegido por um token de API enviado no header `key`.

```bash
curl -X POST "http://localhost:8000/rag?question=Qual%20a%20hipotese%20do%20estudo?&prompt_type=filtered" \
  -H "key: api-tok3n"
```

### Tipos de prompt

O parâmetro `prompt_type` controla a estratégia de geração:

| Tipo | Comportamento |
|------|---------------|
| `default` | Resposta livre do agente, sem recuperação de documentos |
| `filtered` | Recupera os 5 documentos mais relevantes do ChromaDB e gera a resposta com base neles |
| `start` | Geração estruturada (dataclass `AboutScience`) |
| `end` | Geração estruturada (dataclass `AboutCategory`) |

A documentação interativa (Swagger) está disponível em `GET /docs`.

## Configuration

Todas as configurações são feitas via variáveis de ambiente:

| Variável | Descrição | Padrão |
|----------|-----------|--------|
| `API_KEY` | Token de autenticação da API | `api-tok3n` |
| `CHROMA_HOST` | Host do ChromaDB | `0.0.0.0` |
| `CHROMA_PORT` | Porta do ChromaDB | `8000` |
| `CHROMA_SERVER_AUTHN_PROVIDER` | Provider de autenticação do ChromaDB | `chromadb.auth.token_authn.TokenAuthClientProvider` |
| `CHROMA_SERVER_AUTHN_CREDENTIALS` | Credencial de autenticação do ChromaDB | `chr0ma-t0k3n` |
| `CHROMA_AUTH_TOKEN_TRANSPORT_HEADER` | Header de transporte do token | `Authorization` |
| `CHROMA_COLLECTION` | Nome da coleção vetorial | `scientific_collection` |
| `EMBEDDING_MODEL_NAME` | Modelo de embedding | `all-MiniLM-L6-v2` |
| `WEB_SERVER_LINK` | URL do servidor llamafile | `http://172.17.0.1:8080` |
| `WEB_SERVER_KEY` | Token do servidor llamafile | `llamafile-t0k3n` |
| `RAG_N_PREDICT` | Número máximo de tokens gerados | `512` |
| `RAG_TEMPERATURE` | Temperatura de amostragem | `0.65` |
| `LOGFIRE_PROJECT_TOKEN` | Token do projeto Logfire | *(vazio)* |

## Going further

- Veja a implementação do agente RAG em [`src/rag/rag_agent.py`](src/rag/rag_agent.py).
- Personalize os prompts em [`src/rag/prompt_generator.py`](src/rag/prompt_generator.py).
- Consulte as conexões com ChromaDB e llamafile em [`src/connections/`](src/connections/).

## Development

```bash
make lock     # atualiza o poetry.lock
make quality  # roda pre-commit em todos os arquivos
make tests    # roda pytest com cobertura (mínimo 70%)
```

## License

[MIT](LICENSE)
