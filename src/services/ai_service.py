from ai.agent import FleetAgent
from services.analytics_service import AnalyticsService


class AIService:

    def __init__(self):
        self.agent = FleetAgent()
        self.analytics = AnalyticsService()

    def ask(
        self,
        question,
        travels,
        vehicles,
        drivers
    ):

        response = self.agent.answer(question)

        tool = response["tool"]

        if tool == "vehicle_utilization":
            result = self.analytics.vehicle_utilization(
                travels,
                vehicles
            )

        elif tool == "driver_performance":
            result = self.analytics.driver_performance(
                drivers,
                travels
            )

        elif tool == "trip_summary":
            result = self.analytics.trip_summary(
                travels,
                drivers,
                vehicles
            )

        else:
            return response["message"]

        print(response["message"])

        result.orderBy(result["total_trips"].desc()).show(10, truncate=False)

        return result