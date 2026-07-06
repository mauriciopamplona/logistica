from pyspark.sql import DataFrame
from pyspark.sql.functions import current_timestamp, trim, col
from utils.logger import get_logger

logger = get_logger(__name__)

class Transformer:

    def transform(
        self,
        dataframe: DataFrame,
        rules: dict
    ) -> DataFrame:

        dataframe = self.trim_strings(dataframe)

        dataframe = self.handle_null_values(
            dataframe,
            rules.get("null_values", {})
        )

        dataframe = self.remove_duplicates(
            dataframe,
            rules["primary_key"]
        )        

        dataframe = self.add_metadata(dataframe)

        return dataframe

    def trim_strings(self, dataframe: DataFrame) -> DataFrame:

        for field in dataframe.schema.fields:
            if field.dataType.simpleString() == "string":
                dataframe = dataframe.withColumn(
                    field.name,
                    trim(col(field.name))
                )

        return dataframe
    
    def handle_null_values(
        self,
        dataframe,
        replacements
    ):
        if not replacements:
            return dataframe
    
        replacements = {
            key: value
            for key, value in replacements.items()
            if value is not None
        }
    
        if not replacements:
            return dataframe
    
        return dataframe.fillna(replacements)

    def remove_duplicates(
        self,
        dataframe: DataFrame,
        primary_key: list[str]
    ) -> DataFrame:

        deduplicated = dataframe.dropDuplicates(primary_key)
        removed = dataframe.count() - deduplicated.count()

        logger.info(
            f"Trusted layer: removed {removed} duplicated rows {primary_key}."
        )

        return deduplicated
    
    def add_metadata(self, dataframe: DataFrame) -> DataFrame:

        return dataframe.withColumn(
            "ingestion_timestamp",
            current_timestamp()
        )