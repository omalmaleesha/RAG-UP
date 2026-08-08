from dotenv import load_dotenv
import os
from langchain_huggingface import HuggingFaceEmbeddings

load_dotenv()
class EmbeddingService:

    def __init__(self):
        self.embedding = HuggingFaceEmbeddings(
            model_name=os.getenv("EMBEDDING_MODEL")
        )

    def get_embedding(self):
        return self.embedding

    def embed_query(self, text: str):
        return self.embedding.embed_query(text)