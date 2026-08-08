import time
from typing import Dict
from langchain_core.messages import HumanMessage
from ragAiAgent import RagAiAgentState


def route_after_cache(state: RagAiAgentState) -> Dict:
    """
    Cheap rule-based classifier.
    Runs only on cache MISS.
    Returns a dict so the conditional edge can read state["route_decision"].
    """
    start = time.perf_counter()
    print(">>> RouteAfterCacheNode")

    last_msg = state["messages"][-1] if state.get("messages") else None

    if not isinstance(last_msg, HumanMessage):
        decision = "plan_tools"
    else:
        query = last_msg.content.strip().lower()

        # 1. Very short / greeting / small talk
        if len(query.split()) <= 4 and any(w in query for w in [
            "hi", "hello", "hey", "thanks", "thank you", "ok", "okay", "bye"
        ]):
            decision = "direct_generate"

        # 2. Pure generation / creative
        elif any(kw in query for kw in [
            "write", "generate", "create", "compose", "draft",
            "poem", "story", "joke", "summarize this", "rephrase",
            "explain like", "in your own words"
        ]):
            decision = "direct_generate"

        # 3. Explicit tool / knowledge indicators
        elif any(kw in query for kw in [
            "search", "find", "look up", "latest", "current", "today",
            "news", "price", "weather", "stock", "calculate", "compute",
            "code", "run", "execute", "file", "document", "pdf", "excel",
            "what is the", "who is", "when did", "how many"
        ]):
            decision = "plan_tools"

        # 4. Default → safer to plan
        else:
            decision = "plan_tools"

    elapsed = time.perf_counter() - start
    metrics = state.get("metrics", {})
    metrics["route_after_cache"] = elapsed

    return {
        "route_decision": decision,
        "metrics": metrics
    }