# Load previous conversation
# Load summary
# Update state

import time
from typing import Dict
from ragAiAgent import RagAiAgentState


class ConversationMemoryNode:

    def __call__(self, state: RagAiAgentState) -> Dict:
        start = time.perf_counter()

        print(">>> ConversationMemoryNode")
        messages = state.get("messages", [])

        if not messages:
            memory = ""
        else:
            # For now simply join previous messages.
            # Later we can replace this with ConversationSummaryMemory.
            memory = "\n".join(
                f"{msg.type}: {msg.content}"
                for msg in messages[:-1]
            )

        elapsed = time.perf_counter() - start
        metrics = state.get("metrics", {})
        metrics["conversation_memory"] = elapsed
        total_time = state.get("total_time", 0)
        total_time += elapsed

        return {
            "conversation_memory": memory,
            "metrics": metrics,
            "total_time": total_time
        }