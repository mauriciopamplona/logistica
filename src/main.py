from pyspark.sql import SparkSession


def main():

    spark = (
        SparkSession.builder
        .appName("logistica")
        .master("local[*]")
        .getOrCreate()
    )

    print("=" * 60)
    print("Spark Session created successfully!")
    print("=" * 60)

    spark.stop()


if __name__ == "__main__":
    main()