# # Evaluate

# # Is the answer grounded?
# # Is it complete?
# # Is it answering the question?


# # reflection_schema.py
# import time

# from pydantic import BaseModel
# from typing import Dict

# from langchain_core.prompts import ChatPromptTemplate

# from ragAiAgent import RagAiAgentState


# class ReflectionOutput(BaseModel):
#     passed: bool


# REFLECTION_PROMPT = """
# Is this answer sufficient for the user's question?

# Question:
# {question}

# Answer:
# {answer}
# """


# class ReflectionNode:

#     def __init__(self, llm):

#         self.chain = (
#             ChatPromptTemplate.from_template(
#                 REFLECTION_PROMPT
#             )
#             | llm.with_structured_output(ReflectionOutput)
#         )

#     def __call__(self, state: RagAiAgentState) -> Dict:
#         start = time.perf_counter()

#         print(">>> ReflectionNode")

#         result = self.chain.invoke(
#             {
#                 "question": state["user_query"],
#                 "answer": state["final_answer"],
#             }
#         )
#         elapsed = time.perf_counter() - start
#         metrics = state.get("metrics", {})
#         metrics["reflection"] = elapsed

#         return {
#             "reflection_passed": result.passed,
#             "metrics": metrics
#         }



from typing import Dict
import time

from ragAiAgent import RagAiAgentState


class ReflectionNode:

    def __call__(self, state: RagAiAgentState) -> Dict:

        start = time.perf_counter()

        print(">>> ReflectionNode")

        answer = state["final_answer"]

        score = 100

        if "I couldn't find" in answer:
            score = 40

        elapsed = time.perf_counter() - start

        metrics = state.get("metrics", {})
        metrics["reflection"] = elapsed

        return {
            "reflection_passed": True,
            "answer_score": score,
            "metrics": metrics
        }