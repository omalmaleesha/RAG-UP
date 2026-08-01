# store

# Embedding(question)
# Answer


# services/semantic_cache_service.py

from typing import List

from ragAiAgent import RagAiAgentState


class SemanticCacheService:

    def __init__(self, cache_vectorstore):
        self.cache_vectorstore = cache_vectorstore

    def add(
        self,
        question: str,
        answer: str
    ):

        self.cache_vectorstore.add_texts(
            texts=[question],
            metadatas=[
                {
                    "answer": answer
                }
            ]
        )


from typing import Dict


class CacheWriterNode:

    def __init__(
        self,
        semantic_cache_service: SemanticCacheService
    ):
        self.semantic_cache_service = semantic_cache_service

    def __call__(self, state: RagAiAgentState) -> Dict:

        question = state["user_query"]
        answer = state["final_answer"]

        print(">>> CacheWriterNode")

        self.semantic_cache_service.add(
            question=question,
            answer=answer
        )

        return {}