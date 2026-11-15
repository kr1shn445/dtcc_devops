
from src.storage.s3_client import discover_csv_files
from src.ingestion.batch_manager import create_batch_metadata

files = discover_csv_files()

print("Batch Metadata Generation")
print("-------------------------")

if not files:
    print("No CSV files available in S3 landing zone.")
else:
    for file in files:
        metadata = create_batch_metadata(file)

        print("Batch ID:", metadata["batch_id"])
        print("File Name:", metadata["file_name"])
        print("S3 Object:", metadata["s3_key"])
        print("File Size:", metadata["file_size"], "bytes")
        print("Last Modified:", metadata["last_modified"])
        print("Received At:", metadata["received_at"])
        print("Status:", metadata["status"])
        print("Replay Attempt:", metadata["replay_attempt"])
        print("-------------------------")
