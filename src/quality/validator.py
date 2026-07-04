from pyspark.sql import DataFrame
from utils.logger import get_logger

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
    
class ValidationResult:

    def __init__(self, passed: bool, message: str):
        self.passed = passed
        self.message = message        