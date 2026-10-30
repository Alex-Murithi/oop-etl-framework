class ETLError(Exception):
    """Base exception for the ETL framework."""
    pass


class ExtractionError(ETLError):
    """Raised when extraction fails."""
    pass


class ValidationError(ETLError):
    """Raised when validation fails."""
    pass