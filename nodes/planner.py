# This is the brain

# Read user question
# Read conversation memory
# Read previous tool outputs
# Decide next action


# planner_schema.py
from pydantic import BaseModel
from typing import Literal, Dict

from langchain_core.prompts import ChatPromptTemplate

from ragAiAgent import RagAiAgentState


class PlannerOutput(BaseModel):
    enough_information: bool
    selected_tool: Literal["rag", "none"]


PLANNER_PROMPT = """
You are a routing agent.

Rules:
- If there is already retrieved information, choose:
  enough_information=true
  selected_tool="none"

- Otherwise choose:
  enough_information=false
  selected_tool="rag"

Return only the structured output.
"""


class PlannerNode:

    def __init__(self, llm):

        self.chain = (
            ChatPromptTemplate.from_messages(
                [
                    ("system", PLANNER_PROMPT),
                    (
                        "human",
                        """
                        Question:
                        {question}

                        Has Retrieved Documents:
                        {has_documents}

                        Has Tool Results:
                        {has_tool_results}
                        """
                    )
                ]
            )
            | llm.with_structured_output(PlannerOutput)
        )

    def __call__(self, state: RagAiAgentState) -> Dict:

        print(">>> PlannerNode")

        result = self.chain.invoke(
            {
                "question": state["user_query"],
                "has_documents": len(state["retrieved_docs"]) > 0,
                "has_tool_results": len(state["tool_results"]) > 0,
            }
        )

        return {
            "selected_tool": result.selected_tool,
            "enough_information": result.enough_information,
        }