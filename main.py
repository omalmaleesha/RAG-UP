import os

from ragAiAgent import RagAiGraph

from nodes.memory import ConversationMemoryNode
from nodes.semantic_cache import SemanticCacheNode
from nodes.planner import PlannerNode
from nodes.tool_router import ToolRouterNode
from nodes.generator import GenerateAnswerNode
from nodes.reflection import ReflectionNode
from nodes.cache_writer import CacheWriterNode
from nodes.route_after_cache import route_after_cache

from services.calendar_service import CalendarService
from tools.calendar_tool import CalendarTool
from tools.rag_tool import RagTool

from services.embeddings import EmbeddingService
from services.semantic_cache import SemanticCacheService
from services.vectorstore import VectorStoreService
from services.llm import LLMService

llm = LLMService().get_llm()


embedding_service = EmbeddingService()
vector_store_service = VectorStoreService()
semantic_cache_service = SemanticCacheService()
rag_tool = RagTool(vector_store_service)
conversation_memory_node = ConversationMemoryNode()
semantic_cache_node = SemanticCacheNode(
    embedding_service,
    semantic_cache_service
)
planner_node = PlannerNode(llm)
calendar_service = CalendarService()
calendar_tool = CalendarTool(calendar_service)
tool_router_node = ToolRouterNode(
    {
        "rag": rag_tool,
        "calendar": calendar_tool
    }
)

generate_answer_node = GenerateAnswerNode(llm)
reflection_node = ReflectionNode()
cache_writer_node = CacheWriterNode(
    semantic_cache_service
)


def main():
    graph = RagAiGraph(
    conversation_memory_node,
    semantic_cache_node,
    planner_node,
    tool_router_node,
    generate_answer_node,
    reflection_node,
    cache_writer_node,
    route_after_cache
    )
    graph.run()


if __name__ == "__main__":
    main()
