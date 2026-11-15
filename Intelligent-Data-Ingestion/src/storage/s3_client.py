
import boto3
from pathlib import Path

AWS_PROFILE = "ingestion-project"
AWS_REGION = "ap-south-1"
BUCKET_NAME = "intelligent-data-ingetion-demo-2026"
LANDING_PREFIX = "landing/"


def get_s3_client():
    session = boto3.Session(
        profile_name=AWS_PROFILE,
        region_name=AWS_REGION
    )
    return session.client("s3")


def discover_csv_files():
    s3 = get_s3_client()

    paginator = s3.get_paginator("list_objects_v2")

    csv_files = []

    for page in paginator.paginate(
        Bucket=BUCKET_NAME,
        Prefix=LANDING_PREFIX
    ):
        for obj in page.get("Contents", []):
            key = obj["Key"]

            if key.lower().endswith(".csv"):
                csv_files.append({
                    "key": key,
                    "size": obj["Size"],
                    "last_modified": obj["LastModified"]
                })

    return csv_files


def download_file(s3_key, destination):
    s3 = get_s3_client()

    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)

    s3.download_file(
        BUCKET_NAME,
        s3_key,
        str(destination)
    )

    return destination


def route_file(s3_key, is_valid, batch_id):
    """Copy a validated file to its appropriate S3 zone."""

    s3 = get_s3_client()

    file_name = Path(s3_key).name

    # Preserve the original file as raw evidence
    raw_key = f"raw-evidence/{batch_id}/{file_name}"

    # Select destination based on validation result
    if is_valid:
        destination_prefix = "accepted"
    else:
        destination_prefix = "quarantine"

    destination_key = f"{destination_prefix}/{batch_id}/{file_name}"

    # Preserve original evidence
    s3.copy_object(
        Bucket=BUCKET_NAME,
        CopySource={"Bucket": BUCKET_NAME, "Key": s3_key},
        Key=raw_key
    )

    # Copy file to accepted or quarantine zone
    s3.copy_object(
        Bucket=BUCKET_NAME,
        CopySource={"Bucket": BUCKET_NAME, "Key": s3_key},
        Key=destination_key
    )

    return {
        "raw_evidence_key": raw_key,
        "destination_key": destination_key,
        "status": "ACCEPTED" if is_valid else "QUARANTINED"
    }
