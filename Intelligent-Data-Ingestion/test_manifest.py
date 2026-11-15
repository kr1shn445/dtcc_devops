
import pandas as pd

from src.storage.s3_client import discover_csv_files
from src.ingestion.batch_manager import create_batch_metadata
from src.ingestion.manifest import generate_manifest
from src.validation.csv_validator import validate_business_rules

files = discover_csv_files()

if not files:
    print("No files found in S3 landing zone.")
else:
    file_details = next(
        file for file in files
        if file["key"].endswith("transactions_invalid.csv")
    )

    metadata = create_batch_metadata(file_details)

    df = pd.read_csv("data/downloaded/transactions_invalid.csv")
    result = validate_business_rules(df)

    manifest_path, error_path, status = generate_manifest(
        metadata,
        result["errors"]
    )

    print("Manifest Generation Successful")
    print("Batch ID:", metadata["batch_id"])
    print("Status:", status)
    print("Manifest:", manifest_path)
    print("Error Log:", error_path)
    print("Total Errors:", len(result["errors"]))
    print("Uploaded to S3: manifests/")
