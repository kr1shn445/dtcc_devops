
import pandas as pd


def load_csv(file_path):
    """Load a CSV file into a Pandas DataFrame."""
    return pd.read_csv(file_path)


def inspect_csv(file_path):
    """Extract basic information about a CSV file."""

    df = load_csv(file_path)

    return {
        "dataframe": df,
        "columns": list(df.columns),
        "rows": len(df),
        "column_count": len(df.columns),
        "data_types": df.dtypes.astype(str).to_dict(),
        "missing_values": df.isnull().sum().to_dict()
    }


def validate_business_rules(df):
    """Validate mandatory fields and transaction business rules."""

    errors = []

    mandatory_fields = [
        "transaction_id",
        "customer_id",
        "transaction_date",
        "amount",
        "currency",
        "status"
    ]

    allowed_currencies = ["INR"]
    allowed_statuses = ["SUCCESS", "PENDING", "FAILED"]

    for index, row in df.iterrows():
        row_number = index + 2

        # Check mandatory fields
        for field in mandatory_fields:
            if pd.isna(row[field]) or str(row[field]).strip() == "":
                errors.append(
                    f"Row {row_number}: Missing mandatory field '{field}'"
                )

        # Validate transaction amount
        amount = pd.to_numeric(row["amount"], errors="coerce")

        if pd.isna(amount):
            errors.append(f"Row {row_number}: Invalid transaction amount")
        elif amount <= 0:
            errors.append(f"Row {row_number}: Amount must be greater than zero")

        # Validate transaction date
        date = pd.to_datetime(row["transaction_date"], errors="coerce")

        if pd.isna(date):
            errors.append(f"Row {row_number}: Invalid transaction date")

        # Validate currency
        if str(row["currency"]).strip() not in allowed_currencies:
            errors.append(f"Row {row_number}: Unsupported currency")

        # Validate transaction status
        if str(row["status"]).strip() not in allowed_statuses:
            errors.append(f"Row {row_number}: Invalid transaction status")

    return {
        "is_valid": len(errors) == 0,
        "errors": errors
    }


def detect_duplicates(df):
    """Identify duplicate transaction records."""

    duplicate_rows = df[df.duplicated(
        subset=["transaction_id"],
        keep=False
    )]

    return {
        "duplicate_count": len(duplicate_rows),
        "duplicates": duplicate_rows
    }
