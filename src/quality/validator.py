from pyspark.sql import DataFrame
from utils.logger import get_logger
from pyspark.sql.functions import col, trim

logger = get_logger(__name__)

class Validator:

    def validate_not_empty(self, dataframe: DataFrame, dataset_name: str) -> bool:

        rows = dataframe.count()

        if rows == 0:
            logger.error(f"{dataset_name} is empty.")
            return False

        logger.info(f"{dataset_name} OK ({rows} rows).")
        return True
    
    def validate_required_columns(
        self,
        dataframe: DataFrame,
        dataset_name: str,
        required_columns: list[str]
    ) -> bool:
    
        existing_columns = set(dataframe.columns)
        required = set(required_columns)
    
        missing = required - existing_columns
    
        if missing:
            logger.error(
                f"{dataset_name}: Missing required columns: {sorted(missing)}"
            )
            return False
    
        logger.info(f"{dataset_name}: Required columns OK.")
        return True
    
    def validate_required_values(
    self,
    dataframe: DataFrame,
    dataset_name: str,
    required_columns: list[str]
    ) -> bool:

        success = True

        for column_name in required_columns:

            invalid_rows = dataframe.filter(
                col(column_name).isNull() |
                (trim(col(column_name)) == "")
            ).count()

            if invalid_rows > 0:
                logger.error(
                    f"{dataset_name}: Column '{column_name}' has {invalid_rows} null/empty values."
                )
                success = False
            else:
                logger.info(
                    f"{dataset_name}: Column '{column_name}' OK."
                )

        return success

    def validate_primary_key(
        self,
        dataframe,
        dataset_name,
        primary_key
    ):
    
        duplicates = (
            dataframe
            .groupBy(primary_key)
            .count()
            .filter("count > 1")
            .count()
        )
    
        if duplicates > 0:
            logger.error(
                f"{dataset_name}: {duplicates} duplicated primary keys."
            )
            return False
    
        logger.info(f"{dataset_name}: Primary key OK.")
        return True
    
    def validate(
        self,
        dataframe,
        dataset_name,
        rules
    ):
        self.validate_not_empty(
            dataframe,
            dataset_name
        )
        self.validate_required_columns(
            dataframe,
            dataset_name,
            rules["required_columns"]
        )

        self.validate_required_values(
            dataframe,
            dataset_name,
            rules["required_values"]
        )
        
        self.validate_primary_key(
            dataframe,
            dataset_name,
            rules["primary_key"]
        )        