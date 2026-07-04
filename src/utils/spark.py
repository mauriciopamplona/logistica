from pyspark.sql import SparkSession


def get_spark_session(app_name: str, master: str) -> SparkSession:
    """
    Create and return a SparkSession.
    """

    spark = (
        SparkSession.builder
        .appName(app_name)
        .master("local[*]")
        .getOrCreate()
    )

    spark.sparkContext.setLogLevel("WARN")

    return spark