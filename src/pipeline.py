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
            validator.validate_not_empty(vehicles, "Vehicles")
            validator.validate_required_columns(
                vehicles,
                "Vehicles",
                config.quality["vehicles"]["required_columns"]
            )            

            drivers = reader.read_json(config.paths["drivers"])
            validator.validate_not_empty(drivers, "Drivers")          
            validator.validate_required_columns(
                drivers,
                "Drivers",
                config.quality["drivers"]["required_columns"]
            )
            drivers.printSchema()
            print(drivers.columns)

            travels = reader.read_csv(config.paths["travels"])
            validator.validate_not_empty(travels, "Travels")
            validator.validate_required_columns(
                travels,
                "Travels",
                config.quality["travels"]["required_columns"]
            )

            tracking = reader.read_parquet(config.paths["tracking"])
            validator.validate_not_empty(tracking, "Tracking")
            validator.validate_required_columns(
                tracking,
                "Tracking",
                config.quality["tracking"]["required_columns"]
            )            

        finally:
            spark.stop()