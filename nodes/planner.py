# This is the brain

# Read user question
# Read conversation memory
# Read previous tool outputs
# Decide next action


# planner_schema.py
import time
from pydantic import BaseModel
from typing import Literal, Dict
from langchain_core.prompts import ChatPromptTemplate
from ragAiAgent import RagAiAgentState

class PlannerOutput(BaseModel):
    enough_information: bool
    selected_tool: Literal["rag", "calendar","none"]

PLANNER_PROMPT = """
You are a routing agent.

Choose exactly one tool.

Tools:
- rag -> General university questions, policies, fees, admissions.
- calendar -> Dates, exams, registrations, academic schedules.

Rules:
- If has_documents OR has_tool_results is true:
  enough_information=true
  selected_tool="none"

- Otherwise:
  Select the best tool based only on the user's question.

Return only structured output.
"""


class PlannerNode:

    def __init__(self, llm):

        self.chain = (
            ChatPromptTemplate.from_messages(
                [
                    ("system", PLANNER_PROMPT),
                    ("human",
                        """
                        Question: {question}

                        Has Documents: {has_documents}
                        Has Tool Results: {has_tool_results}
                        """
                    )
                ]
            )
            | llm.with_structured_output(PlannerOutput)
        )

    def __call__(self, state: RagAiAgentState) -> Dict:
        start = time.perf_counter()

        print(">>> PlannerNode")

        result = self.chain.invoke(
            {
                "question": state["user_query"],
                "has_documents": len(state["retrieved_docs"]) > 0,
                "has_tool_results": len(state["tool_results"]) > 0,
            }
        )
        elapsed = time.perf_counter() - start
        metrics = state.get("metrics", {})
        metrics["planner"] = elapsed


        return {
            "selected_tool": result.selected_tool,
            "enough_information": result.enough_information,
            "metrics": metrics
        }