import uuid
from datetime import datetime, timezone
from pathlib import Path


def generate_batch_id():
    """Generate a unique identifier for each file delivery."""
    return str(uuid.uuid4())


def create_batch_metadata(file_details):
    """Create metadata for an incoming S3 file."""

    batch_id = generate_batch_id()

    metadata = {
        "batch_id": batch_id,
        "file_name": Path(file_details["key"]).name,
        "s3_key": file_details["key"],
        "file_size": file_details["size"],
        "last_modified": file_details["last_modified"].isoformat(),
        "received_at": datetime.now(timezone.utc).isoformat(),
        "status": "RECEIVED",
        "replay_attempt": 1,
        "parent_batch_id": None
    }

    return metadata