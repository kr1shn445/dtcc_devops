
import os
import boto3
import pandas as pd
import snowflake.connector

from dotenv import load_dotenv
from snowflake.connector.pandas_tools import write_pandas

load_dotenv()

BUCKET = "intelligent-data-ingetion-demo-2026"

# Connect to AWS using your existing CLI profile
session = boto3.Session(
    profile_name="ingestion-project",
    region_name="ap-south-1"
)
s3 = session.client("s3")

# Connect to Snowflake
conn = snowflake.connector.connect(
    account=os.getenv("SNOWFLAKE_ACCOUNT"),
    user=os.getenv("SNOWFLAKE_USER"),
    password=os.getenv("SNOWFLAKE_PASSWORD"),
    warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
    database="INGESTION_DB",
    schema="PUBLIC",
    role="ACCOUNTADMIN"
)

response = s3.list_objects_v2(
    Bucket=BUCKET,
    Prefix="accepted/"
)

files = [
    obj["Key"] for obj in response.get("Contents", [])
    if obj["Key"].endswith(".csv")
]

if not files:
    print("No accepted CSV files found in S3.")
else:
    for key in files:
        print("\nLoading:", key)

        obj = s3.get_object(Bucket=BUCKET, Key=key)
        df = pd.read_csv(obj["Body"])

        batch_id = key.split("/")[1] if len(key.split("/")) > 2 else "UNKNOWN"
        df.columns = [col.upper().strip() for col in df.columns]
        df["BATCH_ID"] = batch_id

        # Keep only columns present in the Snowflake target table
        expected = [
            "TRANSACTION_ID", "CUSTOMER_ID", "TRANSACTION_DATE",
            "AMOUNT", "CURRENCY", "STATUS", "BATCH_ID"
        ]
        df = df[expected]

        success, nchunks, nrows, output = write_pandas(
            conn,
            df,
            table_name="INGESTION_RECORDS",
            database="INGESTION_DB",
            schema="PUBLIC"
        )

        print("Loaded successfully:", success)
        print("Rows loaded:", nrows)

conn.close()
print("\nS3 TO SNOWFLAKE LOADING COMPLETED")
