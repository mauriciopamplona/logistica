from pyspark.sql import DataFrame
from pyspark.sql.functions import count


class VehicleUtilization:

    def build(
        self,
        vehicles: DataFrame,
        travels: DataFrame
    ) -> DataFrame:

        trips = (
            travels
            .groupBy("veiculo_id")
            .agg(
                count("*").alias("total_trips")
            )
        )

        return (
            vehicles
            .join(
                trips,
                "veiculo_id",
                "left"
            )
            .fillna({"total_trips": 0})
        )