from src.storage.s3_client import download_file

s3_key = "landing/transactions.csv"
destination = "data/downloaded/transactions.csv"

try:
    downloaded_file = download_file(s3_key, destination)

    print("S3 File Download Successful!")
    print("S3 Object:", s3_key)
    print("Local File:", downloaded_file)
    print("File Exists:", downloaded_file.exists())

except Exception as error:
    print("Download failed:", error)
