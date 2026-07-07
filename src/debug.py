"""
Development helper.

Starts a Spark session, loads all datasets, and opens an
interactive Python console for testing Spark queries.

Not used by the production pipeline.
"""
import code

from extraction.reader import Reader
from utils.config import Config
from utils.spark import get_spark_session

print("=" * 60)
print("Loading debug environment...")
print("=" * 60)

config = Config()

spark = get_spark_session(
    app_name="debug",
    master=config.spark["master"]
)

reader = Reader(spark)

vehicles = reader.read_csv(config.paths["vehicles"])
drivers = reader.read_json(config.paths["drivers"])
travels = reader.read_csv(config.paths["travels"])
tracking = reader.read_parquet(config.paths["tracking"])

print()
print("Datasets loaded:")
print(f"Vehicles : {vehicles.count()}")
print(f"Drivers  : {drivers.count()}")
print(f"Travels  : {travels.count()}")
print(f"Tracking : {tracking.count()}")

print()
print("Available variables:")
print("""
spark
config
reader
vehicles
drivers
travels
tracking
""")

code.interact(local=locals())