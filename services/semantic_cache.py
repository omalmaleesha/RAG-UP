import os
from dotenv import load_dotenv
from langchain_chroma import Chroma
from services.embeddings import EmbeddingService

load_dotenv()

class SemanticCacheService:

    def __init__(self):
        print("\n" + "=" * 60)
        print(">>> INITIALIZING SEMANTIC CACHE")
        embedding = EmbeddingService().get_embedding()
        persist_directory = os.getenv("SEMANTIC_CACHE_DB")
        print(f"Cache database: {persist_directory}")
        self.cache = Chroma(
            persist_directory=persist_directory,
            embedding_function=embedding
        )
        print("✅ Semantic cache initialized")
        print("=" * 60)


    def add(self,question: str,answer: str):
        print("\n" + "=" * 60)
        print(">>> ADDING TO SEMANTIC CACHE")
        print(f"Question: {question}")
        print(f"Answer length: {len(answer)} characters")

        self.cache.add_texts(
            texts=[question],
            metadatas=[
                {
                    "answer": answer
                }
            ]
        )

        print("✅ Question added to semantic cache")
        print("=" * 60)


    def search(self,query: str,top_k: int = 1):
        print("\n" + "=" * 60)
        print(">>> SEMANTIC CACHE SEARCH")
        print(f"Query: {query}")
        print(f"Top K: {top_k}")

        results = self.cache.similarity_search_with_score(
            query=query,
            k=top_k
        )

        print(f"Results found: {len(results)}")
        output = []
        if not results:
            print("❌ SEMANTIC CACHE MISS")
            print("No matching cache entries found.")
            print("=" * 60)

            return output

        for index, (doc, score) in enumerate(results, start=1):
            print("\n--- CACHE RESULT ---")
            print(f"Result #{index}")
            print(f"Cached question: {doc.page_content}")
            print(f"Score / Distance: {score}")
            print(f"Cached answer length: {len(doc.metadata.get('answer', ''))}")

            output.append(
                {
                    "question": doc.page_content,
                    "answer": doc.metadata["answer"],
                    "score": score
                }
            )

        print("\n✅ SEMANTIC CACHE RESULT FOUND")
        print("=" * 60)
        return output


    def reset(self):
        """Delete all semantic cache entries."""

        print("\n" + "=" * 60)
        print(">>> RESETTING SEMANTIC CACHE")
        data = self.cache.get()
        ids = data.get("ids", [])
        print(f"Cache entries found: {len(ids)}")

        if ids:
            self.cache.delete(ids=ids)

        print(
            f"✅ Semantic cache reset. "
            f"Deleted {len(ids)} entries."
        )

        print("=" * 60)