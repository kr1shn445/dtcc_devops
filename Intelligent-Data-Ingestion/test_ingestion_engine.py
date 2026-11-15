
import pandas as pd

from src.storage.s3_client import (
    discover_csv_files,
    download_file,
    route_file
)
from src.ingestion.batch_manager import create_batch_metadata
from src.ingestion.manifest import generate_manifest
from src.validation.checksum import verify_file_integrity
from src.validation.schema import validate_schema
from src.validation.csv_validator import (
    validate_business_rules,
    detect_duplicates
)

TEST_FILES = [
    {
        "name": "transactions.csv",
        "original": "data/sample/transactions.csv"
    },
    {
        "name": "transactions_invalid.csv",
        "original": "data/sample/transactions_invalid.csv"
    }
]

s3_files = discover_csv_files()

print("END-TO-END INGESTION ENGINE TEST")
print("================================")

for item in TEST_FILES:

    file_details = next(
        (f for f in s3_files if f["key"].endswith(item["name"])),
        None
    )

    if file_details is None:
        print(f"\nFile not found in S3: {item['name']}")
        continue

    local_path = f"data/downloaded/{item['name']}"

    download_file(file_details["key"], local_path)

    metadata = create_batch_metadata(file_details)

    checksum = verify_file_integrity(
        item["original"], local_path
    )

    df = pd.read_csv(local_path)

    schema = validate_schema(df)
    business = validate_business_rules(df)
    duplicates = detect_duplicates(df)

    errors = schema["errors"] + business["errors"]

    is_valid = (
        schema["is_valid"]
        and business["is_valid"]
        and checksum["integrity_verified"]
    )

    routing = route_file(
        file_details["key"],
        is_valid,
        metadata["batch_id"]
    )

    generate_manifest(metadata, errors)

    print(f"\nFile: {item['name']}")
    print("Batch ID:", metadata["batch_id"])
    print("Checksum:", "VERIFIED" if checksum["integrity_verified"] else "FAILED")
    print("Schema:", "VALID" if schema["is_valid"] else "INVALID")
    print("Business Rules:", "VALID" if business["is_valid"] else "INVALID")
    print("Duplicate Records:", duplicates["duplicate_count"])
    print("Validation Errors:", len(errors))
    print("Final Status:", routing["status"])
    print("S3 Destination:", routing["destination_key"])

print("\nINGESTION ENGINE TEST COMPLETED")
