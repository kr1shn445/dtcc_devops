
from src.validation.checksum import verify_file_integrity

original_file = "data/sample/transactions.csv"
downloaded_file = "data/downloaded/transactions.csv"

result = verify_file_integrity(
    original_file,
    downloaded_file
)

print("SHA-256 Checksum Validation")
print("---------------------------")

print("Original SHA-256:", result["original_checksum"])
print("Downloaded SHA-256:", result["downloaded_checksum"])

if result["integrity_verified"]:
    print("Integrity Status: VERIFIED")
    print("Both files are identical.")
else:
    print("Integrity Status: FAILED")
    print("File contents do not match.")
