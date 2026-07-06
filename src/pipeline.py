from extraction.reader import Reader
from utils.config import Config
from utils.spark import get_spark_session
from utils.logger import get_logger
from quality.validator import Validator
from transform.transformer import Transformer
from load.writer import Writer
from output.analytics.analytics import Analytics

logger = get_logger(__name__)

class Pipeline:

    def run(self):

        logger.info("Pipeline started")

        config = Config()
        transformer = Transformer()
        writer = Writer()
        analytics = Analytics()

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

            vehicles = transformer.transform(
                vehicles,
                config.quality["vehicles"]
            )
            
            writer.write(
                vehicles,
                config.output["trusted"]["vehicles"]
            )

            drivers = reader.read_json(config.paths["drivers"])

            validator.validate(
                drivers,
                "Drivers",
                config.quality["drivers"]
            )

            drivers = transformer.transform(
                drivers,
                config.quality["drivers"]
            )

            writer.write(
                drivers,
                config.output["trusted"]["drivers"]
            )            

            travels = reader.read_csv(config.paths["travels"])

            validator.validate(
                travels,
                "Travels",
                config.quality["travels"]
            )

            travels = transformer.transform(
                travels,
                config.quality["travels"]
            )

            writer.write(
                travels,
                config.output["trusted"]["travels"]
            )             

            tracking = reader.read_parquet(config.paths["tracking"])

            validator.validate(
                tracking,
                "Tracking",
                config.quality["tracking"]
            )

            tracking = transformer.transform(
                tracking,
                config.quality["tracking"]
            )

            writer.write(
                tracking,
                config.output["trusted"]["tracking"]
            )

            trip_summary = analytics.build_trip_summary(
                travels,
                drivers,
                vehicles
            )

            writer.write(
                trip_summary,
                config.output["analytics"]["trip_summary"]
            )

        finally:
            spark.stop()