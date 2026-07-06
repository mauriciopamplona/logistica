from pyspark.sql import DataFrame


class Writer:

    def write(
        self,
        dataframe,
        path
    ):

        (
            dataframe.write
            .mode("overwrite")
            .parquet(path)
        )        