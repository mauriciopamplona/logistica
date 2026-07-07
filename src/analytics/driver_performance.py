from pyspark.sql import DataFrame
from pyspark.sql.functions import count


class DriverPerformance:

    def build(
        self,
        drivers: DataFrame,
        travels: DataFrame
    ) -> DataFrame:

        trips = (
            travels
            .groupBy("motorista_id")
            .agg(
                count("*").alias("total_trips")
            )
        )

        return (
            drivers
            .join(
                trips,
                "motorista_id",
                "left"
            )
            .fillna({"total_trips": 0})
            .select(
                "motorista_id",
                "nome",
                "status",
                "base_operacional",
                "data_admissao",
                "total_trips"
            )
        )