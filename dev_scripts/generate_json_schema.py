#!/usr/bin/env python
"""
Generate JSON Schema from the Pydantic models.

This creates a JSON Schema file that can be used for documentation,
validation with other tools, or IDE autocomplete.

Usage:
    python scripts/generate_json_schema.py > schema.json
"""

import json

from congressionalrecord.schema import CongressionalRecordDocument


def main():
    """Generate and print JSON Schema."""
    schema = CongressionalRecordDocument.model_json_schema()

    # Pretty print the schema
    print(json.dumps(schema, indent=2))


if __name__ == "__main__":
    main()
