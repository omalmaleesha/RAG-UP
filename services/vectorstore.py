# services/vector_store.py

import os
from dotenv import load_dotenv

from langchain_chroma import Chroma

from services.embeddings import EmbeddingService

load_dotenv()


class VectorStoreService:

    def __init__(self):

        self.db = Chroma(
            persist_directory=os.getenv("VECTOR_DB"),
            embedding_function=EmbeddingService().get_embedding(),
        )

    def add_documents(self, docs):
        self.db.add_documents(docs)

    def similarity_search(self, query, k=5):
        return self.db.similarity_search(query=query, k=k)

    def reset(self):
        self.db.reset_collection()