# Load previous conversation
# Load summary
# Update state

from typing import Dict
from ragAiAgent import RagAiAgentState


class ConversationMemoryNode:

    def __call__(self, state: RagAiAgentState) -> Dict:
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
        return {
            "conversation_memory": memory
        }