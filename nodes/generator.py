# User Question
# Conversation Memory
# Retrieved Docs
# Tool Results

#using these generate the answer

ANSWER_PROMPT = """
You are a University AI Assistant.

Answer ONLY from the provided context.

If the answer is not in the context, reply:
"I couldn't find that information."

Context:
{context}

Question:
{question}
"""

import time
from typing import Dict

from langchain_core.prompts import ChatPromptTemplate
from ragAiAgent import RagAiAgentState


class GenerateAnswerNode:

    def __init__(self, llm):

        self.chain = (
            ChatPromptTemplate.from_template(ANSWER_PROMPT)
            | llm
        )

    def __call__(self, state: RagAiAgentState) -> Dict:
        start = time.perf_counter()

        print(">>> GenerateAnswerNode")

        documents = "\n\n".join(
            doc.page_content[:600]
            for doc in state["retrieved_docs"][:3]
        )

        response = self.chain.invoke(
            {
                "question": state["user_query"],
                "context": documents
            }
        )
        elapsed = time.perf_counter() - start

        metrics = state.get("metrics", {})
        metrics["generate_answer"] = elapsed

        return {
            "final_answer": response.content,
            "metrics": metrics
        }