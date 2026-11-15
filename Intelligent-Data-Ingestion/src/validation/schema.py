
import pandas as pd

EXPECTED_SCHEMA = {
    "transaction_id": "string",
    "customer_id": "string",
    "transaction_date": "date",
    "amount": "numeric",
    "currency": "string",
    "status": "string"
}


def validate_schema(df):
    """Validate CSV columns and their expected data types."""

    errors = []

    actual_columns = set(df.columns)
    expected_columns = set(EXPECTED_SCHEMA.keys())

    missing_columns = expected_columns - actual_columns
    unexpected_columns = actual_columns - expected_columns

    for column in missing_columns:
        errors.append(f"Missing required column: {column}")

    for column in unexpected_columns:
        errors.append(f"Unexpected column: {column}")

    if "amount" in df.columns:
        invalid_amounts = pd.to_numeric(
            df["amount"], errors="coerce"
        ).isna() & df["amount"].notna()

        if invalid_amounts.any():
            errors.append("Invalid numeric values in amount column")

    if "transaction_date" in df.columns:
        invalid_dates = pd.to_datetime(
            df["transaction_date"], errors="coerce"
        ).isna() & df["transaction_date"].notna()

        if invalid_dates.any():
            errors.append("Invalid date values in transaction_date column")

    for column in ["transaction_id", "customer_id", "currency", "status"]:
        if column in df.columns:
            if not (
                df[column].dropna().map(
                    lambda value: isinstance(value, str)
                ).all()
            ):
                errors.append(f"Invalid data type in {column} column")

    return {
        "is_valid": len(errors) == 0,
        "errors": errors
    }
