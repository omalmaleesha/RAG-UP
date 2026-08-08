# Execute whatever tool planner selected.


from abc import ABC, abstractmethod
from typing import Dict
from ragAiAgent import RagAiAgentState


class BaseTool(ABC):

    @abstractmethod
    def invoke(self, state) -> Dict:
        pass


class ToolRouterNode:

    def __init__(self, tools: Dict):

        """
        tools = {
            "rag": RagTool()
            "calander": CalendarTool()
        }
        """

        self.tools = tools

    def __call__(self, state: RagAiAgentState) -> Dict:
        selected_tool = state["selected_tool"]
        if selected_tool is None:
            raise ValueError("Planner did not select a tool.")

        if selected_tool not in self.tools:
            raise ValueError(f"Unknown tool : {selected_tool}")

        tool = self.tools[selected_tool]

        return tool.invoke(state)