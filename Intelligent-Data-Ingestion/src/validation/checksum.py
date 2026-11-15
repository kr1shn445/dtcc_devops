
import hashlib
from pathlib import Path


def calculate_sha256(file_path):
    """Calculate the SHA-256 checksum of a file."""

    sha256_hash = hashlib.sha256()

    with open(file_path, "rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            sha256_hash.update(chunk)

    return sha256_hash.hexdigest()


def verify_file_integrity(original_file, downloaded_file):
    """Compare checksums of original and downloaded files."""

    original_hash = calculate_sha256(original_file)
    downloaded_hash = calculate_sha256(downloaded_file)

    return {
        "original_checksum": original_hash,
        "downloaded_checksum": downloaded_hash,
        "integrity_verified": original_hash == downloaded_hash
    }
