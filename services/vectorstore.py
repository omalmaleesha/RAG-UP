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
        
        
    def has_documents(self):
        """
        Check whether the vector database contains any documents.
        Returns True if documents exist, otherwise False.
        """
        data = self.db.get()
        count = len(data.get("ids", []))
        has_docs = count > 0

        print(f"Vector DB document count: {count}")
        print(f"Vector DB has documents: {has_docs}")

        return has_docs
    
    
# $ python -c "from services.vectorstore import VectorStoreService; VectorStoreService().has_documents()"
