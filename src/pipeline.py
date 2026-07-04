from extraction.reader import Reader
from utils.config import Config
from utils.spark import get_spark_session
from utils.logger import get_logger

logger = get_logger(__name__)

class Pipeline:

    def log_dataset(self, name, dataframe):
        rows = dataframe.count()
        logger.info(f"{name}: {rows} rows")

    def run(self):

        logger.info("Pipeline started")

        config = Config()

        spark = get_spark_session(
            app_name=config.application["name"],
            master=config.spark["master"]
        )        

        try:

            reader = Reader(spark)

            vehicles = reader.read_csv(config.paths["vehicles"])
            self.log_dataset("Vehicles", vehicles)

            drivers = reader.read_json(config.paths["drivers"])
            self.log_dataset("Drivers", drivers)

            travels = reader.read_csv(config.paths["travels"])
            self.log_dataset("Travels", travels)

            tracking = reader.read_parquet(config.paths["tracking"])
            self.log_dataset("Tracking", tracking)

            vehicles.printSchema()

        finally:
            spark.stop()