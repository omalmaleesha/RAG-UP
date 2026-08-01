# Embed query
# Search semantic cache
# Decide cache hit

import time
from typing import Dict

from ragAiAgent import RagAiAgentState
from services.embeddings import EmbeddingService
from services.semantic_cache import SemanticCacheService


class SemanticCacheNode:

    def __init__(
        self,
        embedding_service: EmbeddingService,
        semantic_cache_service: SemanticCacheService,
        similarity_threshold: float = 0.90
    ):
        self.embedding_service = embedding_service
        self.semantic_cache_service = semantic_cache_service
        self.similarity_threshold = similarity_threshold

    def __call__(self, state: RagAiAgentState) -> Dict:
        start = time.perf_counter()
        print(">>> SemanticCacheNode")

        query = state["user_query"]

        cache_result = self.semantic_cache_service.search(
            query=query,
            top_k=1
        )

        print(f"Cache result: {cache_result}")

        if not cache_result:

            elapsed = time.perf_counter() - start
            metrics = state.get("metrics", {})
            metrics["semantic_cache"] = elapsed

            return {
                "cache_hit": False,
                "cached_answer": None,
                "metrics": metrics
            }

        best_match = cache_result[0]

        distance_threshold = 0.5

        if best_match["score"] <= distance_threshold:

            print(f"Best match: {best_match}")

            elapsed = time.perf_counter() - start
            metrics = state.get("metrics", {})
            metrics["semantic_cache"] = elapsed

            return {
                "cache_hit": True,
                "cached_answer": best_match["answer"],
                "final_answer": best_match["answer"],
                "metrics": metrics
            }

        elapsed = time.perf_counter() - start
        metrics = state.get("metrics", {})
        metrics["semantic_cache"] = elapsed
        

        return {
            "cache_hit": False,
            "cached_answer": None,
            "metrics": metrics
        }