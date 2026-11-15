
import uuid
import pandas as pd

from src.storage.s3_client import route_file
from src.validation.schema import validate_schema
from src.validation.csv_validator import validate_business_rules


test_files = [
    {
        "name": "transactions.csv",
        "key": "landing/transactions.csv",
        "local_path": "data/downloaded/transactions.csv"
    },
    {
        "name": "transactions_invalid.csv",
        "key": "landing/transactions_invalid.csv",
        "local_path": "data/downloaded/transactions_invalid.csv"
    }
]

for file in test_files:
    df = pd.read_csv(file["local_path"])

    schema_result = validate_schema(df)
    business_result = validate_business_rules(df)

    is_valid = (
        schema_result["is_valid"]
        and business_result["is_valid"]
    )

    batch_id = str(uuid.uuid4())

    result = route_file(
        file["key"],
        is_valid,
        batch_id
    )

    print("\nFile:", file["name"])
    print("Validation:", "VALID" if is_valid else "INVALID")
    print("Routing Status:", result["status"])
    print("Raw Evidence:", result["raw_evidence_key"])
    print("Destination:", result["destination_key"])