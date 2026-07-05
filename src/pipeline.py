from extraction.reader import Reader
from utils.config import Config
from utils.spark import get_spark_session
from utils.logger import get_logger
from quality.validator import Validator

logger = get_logger(__name__)

class Pipeline:

    def run(self):

        logger.info("Pipeline started")

        config = Config()

        spark = get_spark_session(
            app_name=config.application["name"],
            master=config.spark["master"]
        )        

        try:

            reader = Reader(spark)

            validator = Validator()

            vehicles = reader.read_csv(config.paths["vehicles"])
            validator.validate(
                vehicles,
                "Vehicles",
                config.quality["vehicles"]
            )           

            drivers = reader.read_json(config.paths["drivers"])
            validator.validate(
                drivers,
                "Drivers",
                config.quality["drivers"]
            )

            travels = reader.read_csv(config.paths["travels"])
            validator.validate(
                travels,
                "Travels",
                config.quality["travels"]
            )

            tracking = reader.read_parquet(config.paths["tracking"])
            validator.validate(
                tracking,
                "Tracking",
                config.quality["tracking"]
            )
        finally:
            spark.stop()