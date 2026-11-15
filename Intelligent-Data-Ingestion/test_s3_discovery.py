
from src.storage.s3_client import discover_csv_files

files = discover_csv_files()

print("S3 File Discovery Results")
print("-------------------------")

if not files:
    print("No CSV files found in the landing zone.")
else:
    for file in files:
        print("File:", file["key"])
        print("Size:", file["size"], "bytes")
        print("Last Modified:", file["last_modified"])
        print("-------------------------")