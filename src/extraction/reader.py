from pyspark.sql import DataFrame, SparkSession


class Reader:
    """
    Responsible only for reading datasets.
    """

    def __init__(self, spark: SparkSession):
        self.spark = spark

    def read_csv(self, path: str) -> DataFrame:
        return (
            self.spark.read
            .option("header", "true")
            .option("inferSchema", "true")
            .csv(path)
        )

    def read_json(self, path: str) -> DataFrame:
        return self.spark.read.json(path)

    def read_parquet(self, path: str) -> DataFrame:
        return self.spark.read.parquet(path)

    def read_geojson(self, path: str):
        raise NotImplementedError("GeoJSON reader will be implemented later.")