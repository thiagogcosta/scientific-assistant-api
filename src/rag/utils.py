from chromadb import Collection
from chromadb.utils import embedding_functions


def get_embedding_function(*, embedding_model_name: str):
    return embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name=embedding_model_name
    )


def get_embeddings(
    *,
    text: str,
    embedding_function: embedding_functions.SentenceTransformerEmbeddingFunction,
):
    return embedding_function([text])[0]


def search_documents(
    *,
    question: str,
    collection: Collection,
    n_results: int = 5,
):
    return collection.query(
        query_texts=question,
        n_results=n_results,
        include=['metadatas', 'documents', 'embeddings'],
    )


def format_search_result(*, relevant_documents):
    formatted_list = []
    for i, doc in enumerate(relevant_documents['documents'][0]):
        formatted_list.append(
            '[{}]: {}'.format(relevant_documents['metadatas'][0][i]['source'], doc)
        )

    documents_str = '\n'.join(formatted_list)
    return documents_str
