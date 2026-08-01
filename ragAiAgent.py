from typing import Annotated, Optional, TypedDict, List, Dict, Any
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, END


class RagAiAgentState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]
    user_query: str
    conversation_memory: Optional[str]
    cache_hit: bool
    cached_answer: Optional[str]
    retrieved_docs: List[Dict[str, Any]]
    selected_tool: Optional[str]
    tool_results: Dict[str, Any]
    planner_reasoning: Optional[str]
    enough_information: bool
    final_answer: Optional[str]
    reflection_passed: bool


def semantic_cache_router(state: RagAiAgentState):

    if state["cache_hit"]:
        return "end"

    return "planner"


def planner_router(state: RagAiAgentState):

    if state["enough_information"]:
        return "generate_answer"

    return "tool_router"

def reflection_router(state: RagAiAgentState):

    if state["reflection_passed"]:
        return "cache_writer"

    return "planner"


class RagAiGraph:

    def __init__(
        self,
        conversation_memory_node,
        semantic_cache_node,
        planner_node,
        tool_router_node,
        generate_answer_node,
        reflection_node,
        cache_writer_node,
    ):

        workflow = StateGraph(RagAiAgentState)
        workflow.add_node(
            "conversation_memory",
            conversation_memory_node
        )
        workflow.add_node(
            "semantic_cache",
            semantic_cache_node
        )
        workflow.add_node(
            "planner",
            planner_node
        )
        workflow.add_node(
            "tool_router",
            tool_router_node
        )
        workflow.add_node(
            "generate_answer",
            generate_answer_node
        )
        workflow.add_node(
            "reflection",
            reflection_node
        )
        workflow.add_node(
            "cache_writer",
            cache_writer_node
        )

        workflow.set_entry_point(
            "conversation_memory"
        )
        workflow.add_edge(
            "conversation_memory",
            "semantic_cache"
        )
        workflow.add_edge(
            "tool_router",
            "planner"
        )
        workflow.add_edge(
            "generate_answer",
            "reflection"
        )
        workflow.add_edge(
            "cache_writer",
            END
        )

        workflow.add_conditional_edges(
            "semantic_cache",
            semantic_cache_router,
            {
                "planner": "planner",
                "end": END,
            },
        )

        workflow.add_conditional_edges(
            "planner",
            planner_router,
            {
                "tool_router": "tool_router",
                "generate_answer": "generate_answer",
            },
        )

        workflow.add_conditional_edges(
            "reflection",
            reflection_router,
            {
                "planner": "planner",
                "cache_writer": "cache_writer",
            },
        )

        self.graph = workflow.compile()


    def run(self):
        user_input = ""

        while (user_input.lower() not in ["exit", "quit"]):

            user_input = input("You: ")

            if user_input.lower() in ["exit", "quit"]:
                    break

            result = self.graph.invoke(
                {
                    "messages": [],
                    "user_query": user_input,
                    "conversation_memory": None,
                    "cache_hit": False,
                    "cached_answer": None,
                    "retrieved_docs": [],
                    "selected_tool": None,
                    "tool_results": {},
                    "planner_reasoning": None,
                    "enough_information": False,
                    "final_answer": None,
                    "reflection_passed": False,
                }
            )

            print("\nAI:", result["final_answer"])