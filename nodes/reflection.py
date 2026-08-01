# Evaluate

# Is the answer grounded?
# Is it complete?
# Is it answering the question?


# reflection_schema.py
from pydantic import BaseModel
from typing import Dict

from langchain_core.prompts import ChatPromptTemplate

from ragAiAgent import RagAiAgentState


class ReflectionOutput(BaseModel):
    passed: bool


REFLECTION_PROMPT = """
Is this answer sufficient for the user's question?

Question:
{question}

Answer:
{answer}
"""


class ReflectionNode:

    def __init__(self, llm):

        self.chain = (
            ChatPromptTemplate.from_template(
                REFLECTION_PROMPT
            )
            | llm.with_structured_output(ReflectionOutput)
        )

    def __call__(self, state: RagAiAgentState) -> Dict:

        print(">>> ReflectionNode")

        result = self.chain.invoke(
            {
                "question": state["user_query"],
                "answer": state["final_answer"],
            }
        )

        return {
            "reflection_passed": result.passed
        }