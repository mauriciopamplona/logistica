from analytics.vehicle_utilization import VehicleUtilization
from analytics.driver_performance import DriverPerformance
from analytics.trip_summary import TripSummary


class AnalyticsService:

    def vehicle_utilization(self, travels, vehicles):
        return VehicleUtilization().build(
        travels,
        vehicles
        )

    def driver_performance(self, drivers, travels):
        return DriverPerformance().build(
            drivers,
            travels
        )

    def trip_summary(self, travels, drivers, vehicles):
        return TripSummary().build(
            travels,
            drivers,
            vehicles
        )