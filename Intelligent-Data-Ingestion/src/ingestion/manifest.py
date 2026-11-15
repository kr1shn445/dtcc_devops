
import json
from pathlib import Path

from src.storage.s3_client import get_s3_client, BUCKET_NAME


def generate_manifest(metadata, validation_errors):
    """Generate and store a batch manifest and error log."""

    batch_id = metadata["batch_id"]

    output_dir = Path("data/manifests")
    output_dir.mkdir(parents=True, exist_ok=True)

    status = "ACCEPTED" if not validation_errors else "QUARANTINED"

    manifest = {
        **metadata,
        "status": status,
        "validation_error_count": len(validation_errors),
        "validation_errors": validation_errors
    }

    manifest_path = output_dir / f"{batch_id}.json"
    error_path = output_dir / f"{batch_id}_errors.txt"

    with open(manifest_path, "w", encoding="utf-8") as file:
        json.dump(manifest, file, indent=4)

    with open(error_path, "w", encoding="utf-8") as file:
        if validation_errors:
            file.write("\n".join(validation_errors))
        else:
            file.write("No validation errors.")

    s3 = get_s3_client()

    s3.upload_file(
        str(manifest_path),
        BUCKET_NAME,
        f"manifests/{batch_id}.json"
    )

    s3.upload_file(
        str(error_path),
        BUCKET_NAME,
        f"manifests/{batch_id}_errors.txt"
    )

    return manifest_path, error_path, status
