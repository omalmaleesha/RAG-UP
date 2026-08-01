# services/vector_store.py

import os
from dotenv import load_dotenv

from langchain_chroma import Chroma

from services.embeddings import EmbeddingService

load_dotenv()


class VectorStoreService:

    def __init__(self):

        embedding = EmbeddingService().get_embedding()

        self.vector_store = Chroma(
            persist_directory=os.getenv("VECTOR_DB"),
            embedding_function=embedding
        )

    def similarity_search(
        self,
        query: str,
        k: int = 5
    ):

        return self.vector_store.similarity_search(
            query=query,
            k=k
        )