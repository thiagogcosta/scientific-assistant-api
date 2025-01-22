ARG PYTHON_IMAGE_VERSION="3.11"

FROM python:${PYTHON_IMAGE_VERSION}-slim

# REF: https://github.com/oobabooga/text-generation-webui/issues/1534#issuecomment-1945967730
RUN apt-get update \
    && apt-get install build-essential python3-dev -y \
    && apt-get install gcc-11 -y

#------------------------------
# DESC: connect and persist information on ChromaDB
#---------------DEVELOPMENT INFOS---------------
ARG CHROMA_HOST='0.0.0.0'
ENV CHROMA_HOST=${CHROMA_HOST}

ARG CHROMA_PORT='8000'
ENV CHROMA_PORT=${CHROMA_PORT}

ARG CHROMA_SERVER_AUTHN_PROVIDER='chromadb.auth.token_authn.TokenAuthClientProvider'
ENV CHROMA_SERVER_AUTHN_PROVIDER=${CHROMA_SERVER_AUTHN_PROVIDER}

ARG CHROMA_SERVER_AUTHN_CREDENTIALS='chr0ma-t0k3n'
ENV CHROMA_SERVER_AUTHN_CREDENTIALS=${CHROMA_SERVER_AUTHN_CREDENTIALS}

ARG CHROMA_AUTH_TOKEN_TRANSPORT_HEADER='Authorization'
ENV CHROMA_AUTH_TOKEN_TRANSPORT_HEADER=${CHROMA_AUTH_TOKEN_TRANSPORT_HEADER}

ARG CHROMA_COLLECTION='scientific_collection'
ENV CHROMA_COLLECTION=${CHROMA_COLLECTION}

ARG EMBEDDING_MODEL_NAME='all-MiniLM-L6-v2'
ENV EMBEDDING_MODEL_NAME=${EMBEDDING_MODEL_NAME}

ARG LOGFIRE_PROJECT_TOKEN=''
ENV LOGFIRE_PROJECT_TOKEN=${LOGFIRE_PROJECT_TOKEN}

#------------------------------

#------------------------------
# DESC: Envs llama web server

ARG WEB_SERVER_LINK='http://172.17.0.1:8080'
ENV WEB_SERVER_LINK=${WEB_SERVER_LINK}

ARG WEB_SERVER_KEY='llamafile-t0k3n'
ENV WEB_SERVER_KEY=${WEB_SERVER_KEY}
#------------------------------

#------------------------------
# DESC: RAG API

ARG API_KEY='api-tok3n'
ENV API_KEY=${API_KEY}

# DESC: é importante ser o mesmo do configurado no Llama Web server
ARG RAG_N_PREDICT='512'
ENV RAG_N_PREDICT=${RAG_N_PREDICT}

ARG RAG_TEMPERATURE='0.65'
ENV RAG_TEMPERATURE=${RAG_TEMPERATURE}

#------------------------------

#------------------------------
# DESC: Config llama-cpp

# REF: https://github.com/oobabooga/text-generation-webui/issues/1534#issuecomment-1945967730
ARG CMAKE_ARGS='-DLLAMA_OPENBLAS=on'
ENV CMAKE_ARGS=${CMAKE_ARGS}

ARG FORCE_CMAKE='1'
ENV FORCE_CMAKE=${FORCE_CMAKE}

#------------------------------

WORKDIR /scientific-assistant-api

RUN chmod -R 775 ./

ENV PYTHONPATH="/scientific-assistant-api"

COPY pyproject.toml poetry.lock ./

# DESC: Install the poetry, set the env var in the project directory,
# and install the dependencies
# REF: https://github.com/oobabooga/text-generation-webui/issues/1534#issuecomment-1945967730
RUN python -m pip install -q poetry==1.8.3 \
    && pip install llama-cpp-python==0.3.0 --no-cache-dir \
    && python -m poetry config virtualenvs.in-project true \
    && python -m poetry install --only main --no-interaction --no-ansi

COPY /scripts ./scripts

# DESC: Get the embedding model
RUN python -m poetry run python ./scripts/caching_embedding_model.py

COPY /src ./src

EXPOSE 8080

RUN chmod +x ./scripts/entrypoint.sh

ENTRYPOINT ["/scientific-assistant-api/scripts/entrypoint.sh"]

#----------INSTRUCTIONS----------

# buildar a imagem
#docker build -t scientific_assistant_api .

# executar o container com os containers visualizando a rede da maquina
#docker run -d --name api_service --network host scientific_assistant_api

# acessar o container
#docker exec -i -t api_service bash

# finalizar a execucao do container
#docker kill api_service

# excluir os containers finalizados
#docker rm $(docker ps -a -q)
