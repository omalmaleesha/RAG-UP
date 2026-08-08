# User Question
# Conversation Memory
# Retrieved Docs
# Tool Results

#using these generate the answer

ANSWER_PROMPT = """
You answer university questions.

Use ONLY this context.

{context}

Question:
{question}

If the answer is missing, say:
"I couldn't find that information."
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

        context_parts = []

        # RAG
        if state["retrieved_docs"]:
            context_parts.append(
                "\n".join(
                    doc.page_content[:400]
                    for doc in state["retrieved_docs"][:2]
                )
            )

        # Other tools
        if state["tool_results"]:
            context_parts.append(str(state["tool_results"]))

        context = "\n\n".join(context_parts)

        response = self.chain.invoke(
            {
                "question": state["user_query"],
                "context": context
            }
        )
        elapsed = time.perf_counter() - start

        metrics = state.get("metrics", {})
        metrics["generate_answer"] = elapsed

        #print(state["tool_results"])

        # -----------------------------
        # TOKEN USAGE
        # -----------------------------
        print("\n--- LLM USAGE ---")

        # print("Response metadata:")
        # print(response.response_metadata)

        usage = getattr(response, "usage_metadata", None)

        if usage:
            input_tokens = usage.get("input_tokens", 0)
            output_tokens = usage.get("output_tokens", 0)
            total_tokens = usage.get("total_tokens", 0)

            print("Input tokens:", input_tokens)
            print("Output tokens:", output_tokens)
            print("Total tokens:", total_tokens)

        else:
            print("Token usage not available")

        return {
            "final_answer": response.content,
            "metrics": metrics
        }