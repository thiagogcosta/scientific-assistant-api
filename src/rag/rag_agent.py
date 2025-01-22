from chromadb import Collection
from llama_cpp_agent import LlamaCppAgent, MessagesFormatterType, StructuredOutputAgent
from llama_cpp_agent.providers import LlamaCppServerProvider
from pydantic import BaseModel

from src.rag.utils import format_search_result, search_documents
from src.templates.rag_agent_base import RagAgentBase


# RagAgent
class RagAgent(RagAgentBase):
    def get_agent(self, *, provider: LlamaCppServerProvider, prompt: str):
        return LlamaCppAgent(
            provider,
            system_prompt=prompt,
            predefined_messages_formatter_type=MessagesFormatterType.PHI_3,
        )

    def retrieve(
        self,
        *,
        user_input: str,
        collection: Collection,
        prompt: str,
    ):
        relevant_documents = search_documents(
            question=user_input,
            collection=collection,
            n_results=5,
        )

        documents_str = format_search_result(relevant_documents=relevant_documents)

        return prompt.format(documents=documents_str)

    def generation(self, *, agent: LlamaCppAgent, settings, user_input: str, prompt):
        return agent.get_chat_response(
            user_input,
            llm_sampling_settings=settings,
            system_prompt=prompt,
            add_message_to_chat_history=False,
            add_response_to_chat_history=False,
        )

    def structured_generation(
        self, *, provider: LlamaCppServerProvider, dataclass: BaseModel, question: str
    ):
        structured_output_agent = StructuredOutputAgent(
            provider,
            debug_output=True,
            messages_formatter_type=MessagesFormatterType.PHI_3,
        )

        return structured_output_agent.create_object(dataclass, question)
