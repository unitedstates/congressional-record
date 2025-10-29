#!/usr/bin/env python
"""
Example script demonstrating how to validate Congressional Record JSON files
using the Pydantic schema.

Usage:
    # Validate a single file with detailed output
    python scripts/validate_json.py output/2025/CREC-2025-01-30/json/CREC-2025-01-30-pt1-PgS524.json

    # Validate all JSON files in a directory
    python scripts/validate_json.py output/2025/CREC-2025-01-30/json/
"""

import json
import sys
from pathlib import Path

from congressionalrecord.schema import CongressionalRecordDocument


def validate_file(filepath: str, verbose: bool = True) -> tuple[bool, str | None]:
    """
    Validate a Congressional Record JSON file against the schema.

    Args:
        filepath: Path to the JSON file
        verbose: If True, print detailed output; if False, only return success/error

    Returns:
        Tuple of (success: bool, error_message: str | None)
    """
    try:
        with open(filepath) as f:
            data = json.load(f)

        doc = CongressionalRecordDocument(**data)

        if verbose:
            print(f"✓ Valid Congressional Record document")
            print(f"  ID: {doc.id}")
            print(f"  Chamber: {doc.header.chamber}")
            print(f"  Date: {doc.header.month} {doc.header.day}, {doc.header.year}")
            print(f"  Volume {doc.header.vol}, Number {doc.header.num}")
            print(f"  Pages: {doc.header.pages}")
            print(f"  Title: {doc.title or doc.doc_title}")
            print(f"  Content items: {len(doc.content)}")

            # Count speeches vs other items
            speeches = [item for item in doc.content if item.kind == "speech"]
            print(f"  Speeches: {len(speeches)}")

            # Count items with bioguide IDs
            with_bioguide = [
                item for item in doc.content if item.speaker_bioguide is not None
            ]
            print(f"  Items with bioguide IDs: {len(with_bioguide)}")

            # Show related bills if any
            if doc.related_bills:
                print(f"  Related bills: {len(doc.related_bills)}")
                for bill in doc.related_bills[:3]:  # Show first 3
                    print(f"    - {bill.type} {bill.number} (Congress {bill.congress})")

        return (True, None)

    except Exception as e:
        error_msg = str(e)
        if verbose:
            print(f"✗ Validation failed: {error_msg}")
        return (False, error_msg)


def validate_directory(dirpath: Path) -> None:
    """Validate all JSON files in a directory."""
    json_files = list(dirpath.glob("*.json"))

    if not json_files:
        print(f"No JSON files found in {dirpath}")
        sys.exit(1)

    print(f"Validating {len(json_files)} JSON files in {dirpath}...")
    print()

    failures = []
    success_count = 0

    for json_file in json_files:
        success, error = validate_file(str(json_file), verbose=False)
        if success:
            success_count += 1
        else:
            failures.append((json_file.name, error))

    # Report failures
    if failures:
        print("Failed validations:")
        for filename, error in failures:
            print(f"  ✗ {filename}")
            print(f"    Error: {error}")
        print()

    # Report summary
    print(f"Successfully validated: {success_count}/{len(json_files)} files")

    if failures:
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)

    path = Path(sys.argv[1])
    if not path.exists():
        print(f"Error: Path not found: {path}")
        sys.exit(1)

    if path.is_dir():
        validate_directory(path)
    elif path.is_file():
        success, _ = validate_file(str(path), verbose=True)
        if not success:
            sys.exit(1)
    else:
        print(f"Error: {path} is not a file or directory")
        sys.exit(1)
