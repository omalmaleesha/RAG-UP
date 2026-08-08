from typing import Dict
from ragAiAgent import RagAiAgentState
from rapidfuzz import fuzz

class CalendarTool:

    def __init__(self, calendar_service):
        self.calendar_service = calendar_service

    def invoke(self, state: RagAiAgentState) -> Dict:
        query = state["user_query"].lower()
        words = query.split()
        results = []
        for event in self.calendar_service.get_events():
            title = event["title"]
            score = fuzz.partial_ratio(
                query.lower(),
                title.lower()
            )
            if score > 70:
                results.append(event)

        print(state["user_query"])
        print(results)

        return {
            "tool_results": {
                "calendar": results
            }
        }