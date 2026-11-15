
import boto3
from botocore.exceptions import ClientError

# AWS project configuration
AWS_PROFILE = "ingestion-project"
AWS_REGION = "ap-south-1"
BUCKET_NAME = "intelligent-data-ingetion-demo-2026"

try:
    # Create an AWS session using the configured profile
    session = boto3.Session(
        profile_name=AWS_PROFILE,
        region_name=AWS_REGION
    )

    # Create an S3 client
    s3 = session.client("s3")

    # Verify bucket access
    response = s3.list_objects_v2(
        Bucket=BUCKET_NAME,
        Delimiter="/"
    )

    print("AWS connection successful!")
    print(f"Bucket: {BUCKET_NAME}")
    print("\nProject folders:")

    # Display the top-level S3 prefixes
    for prefix in response.get("CommonPrefixes", []):
        print("-", prefix["Prefix"])

except ClientError as error:
    print("AWS S3 operation failed:")
    print(error)

except Exception as error:
    print("Connection failed:")
    print(error)
