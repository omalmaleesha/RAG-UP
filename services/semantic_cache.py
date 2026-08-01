import os
from dotenv import load_dotenv

from langchain_chroma import Chroma

from services.embeddings import EmbeddingService

load_dotenv()


class SemanticCacheService:

    def __init__(self):

        embedding = EmbeddingService().get_embedding()

        self.cache = Chroma(
            persist_directory=os.getenv("SEMANTIC_CACHE_DB"),
            embedding_function=embedding
        )

    def add(
        self,
        question: str,
        answer: str
    ):

        self.cache.add_texts(
            texts=[question],
            metadatas=[
                {
                    "answer": answer
                }
            ]
        )

    def search(
        self,
        query: str,
        top_k: int = 1
    ):

        results = self.cache.similarity_search_with_score(
            query=query,
            k=top_k
        )

        output = []

        for doc, score in results:

            output.append(
                {
                    "question": doc.page_content,
                    "answer": doc.metadata["answer"],
                    "score": score
                }
            )

        return output