# The RAG Tool only retrieves information. It never generates an answer.
# tools/rag_tool.py
# this is an normal rag not yet connected the original RAG AI chatbot in My old project

from typing import Dict
from ragAiAgent import RagAiAgentState
from services.vectorstore import VectorStoreService

class RagTool:

    def __init__(self, vector_store: VectorStoreService):
        self.vector_store = vector_store

    def invoke(self, state: RagAiAgentState) -> Dict:
        query = state["user_query"]
        documents = self.vector_store.similarity_search(
            query=query,
            k=5
        )

        return {
            "retrieved_docs": documents,
            "tool_results": {
                **state["tool_results"],
                "rag": documents
            }

        }