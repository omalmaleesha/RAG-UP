import json
class CalendarService:

    def __init__(self):
        with open("data/calendar.json", "r") as f:
            self.events = json.load(f)

    def get_events(self):
        print(">>>CALENDAR SERVICE USED")
        return self.events