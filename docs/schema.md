# Congressional Record JSON Schema

This document describes the structure of the JSON files produced by the congressional record parser.

## Overview

The parser converts HTML files from the Congressional Record into structured JSON documents. Each JSON file represents a section of the Congressional Record (e.g., a page or range of pages).

## Pydantic Models

The schema is defined using [Pydantic](https://pydantic.dev/) models in `congressionalrecord/schema.py`. These models provide:

- **Type safety**: Automatic validation of JSON structure
- **Documentation**: Field descriptions and examples
- **IDE support**: Autocomplete and type checking
- **JSON Schema generation**: Can export to standard JSON Schema format

## Schema Structure

### Top-Level Document

A `CongressionalRecordDocument` contains:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | Yes | Unique identifier (e.g., "CREC-2025-01-30-pt1-PgS520") |
| `header` | Header | Yes | Metadata about the Congressional Record issue |
| `doc_title` | string | Yes | Title from metadata |
| `title` | string | No | Title parsed from content (all-caps heading) |
| `content` | ContentItem[] | Yes | List of content items (speeches, notes, etc.) |
| `related_bills` | RelatedBill[] | No | Bills referenced in this document |
| `related_laws` | RelatedLaw[] | No | Laws referenced in this document |
| `related_usc` | RelatedUSC[] | No | U.S. Code sections referenced |
| `related_statute` | RelatedStatute[] | No | Statutes at Large referenced |

### Header

Contains metadata about the Congressional Record issue:

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `vol` | string | Volume number | "171" |
| `num` | string | Issue number | "20" |
| `wkday` | string | Day of week | "Thursday" |
| `month` | string | Month name | "January" |
| `day` | string | Day of month | "30" |
| `year` | string | Year | "2025" |
| `chamber` | string | Chamber of Congress | "Senate" or "House" |
| `pages` | string | Page range | "S520-S523" |
| `extension` | boolean | Is Extensions of Remarks? | false |

### ContentItem

Represents a single piece of content (speech, procedural note, etc.):

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `kind` | string | Yes | Type of item (see below) |
| `speaker` | string | Yes | Speaker name or "Unknown" |
| `speaker_bioguide` | string | No | Bioguide ID if matched to a member |
| `text` | string | Yes | Full text content |
| `turn` | integer | Yes | Turn number (for speeches) or -1 |
| `itemno` | integer | Yes | Sequential item number in document |

#### Content Item Types (`kind`)

- `speech`: A member's speech or statement
- `recorder`: Procedural text by the recorder/clerk
- `clerk`: Text read by the clerk
- `linebreak`: Visual separator in the record
- `excerpt`: Quoted or inserted material
- `rollcall`: Roll call vote information
- `metacharacters`: Internal markers (timestamps, page breaks)
- `empty_line`: Empty lines (usually skipped)
- `title`: Section title
- `Unknown`: Could not be classified

### RelatedBill

Reference to a bill mentioned in the Congressional Record:

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `congress` | string | Congress number | "119" |
| `context` | string | Context of reference | "OTHER" |
| `number` | string | Bill number | "47" |
| `type` | string | Bill type | "SRES" (Senate Resolution) |

### Related Laws, USC, and Statutes

These models are placeholders for future enhancement based on actual XML structure in the source data.

## Usage Examples

### Python Validation

```python
import json
from congressionalrecord.schema import CongressionalRecordDocument

# Load and validate a JSON file
with open('output/2025/CREC-2025-01-30/json/CREC-2025-01-30-pt1-PgS524.json') as f:
    data = json.load(f)

doc = CongressionalRecordDocument(**data)

# Access typed fields
print(f"Chamber: {doc.header.chamber}")
print(f"Date: {doc.header.month} {doc.header.day}, {doc.header.year}")

# Iterate over content
for item in doc.content:
    if item.kind == "speech" and item.speaker_bioguide:
        print(f"{item.speaker} (Bioguide: {item.speaker_bioguide})")
```

### Command-Line Validation

Use the provided validation script:

```bash
uv run python dev_scripts/validate_json.py output/2025/CREC-2025-01-30/json/CREC-2025-01-30-pt1-PgS524.json
```

### Generate JSON Schema

Export to standard JSON Schema format for use with other tools:

```bash
uv run python dev_scripts/generate_json_schema.py > schema.json
```

## Example Document

```json
{
  "id": "CREC-2025-01-30-pt1-PgS524",
  "header": {
    "vol": "171",
    "num": "20",
    "wkday": "Thursday",
    "month": "January",
    "day": "30",
    "year": "2025",
    "chamber": "Senate",
    "pages": "S524",
    "extension": false
  },
  "doc_title": "SUBMISSION OF CONCURRENT AND SENATE RESOLUTIONS",
  "title": "SUBMISSION OF CONCURRENT AND SENATE RESOLUTIONS",
  "content": [
    {
      "kind": "Unknown",
      "speaker": "Unknown",
      "speaker_bioguide": null,
      "text": "The following concurrent resolutions and Senate resolutions were read...",
      "turn": -1,
      "itemno": 0
    },
    {
      "kind": "recorder",
      "speaker": "The RECORDER",
      "speaker_bioguide": null,
      "text": "By Ms. HIRONO (for herself, Ms. Duckworth, Mr. Blumenthal...)",
      "turn": -1,
      "itemno": 1
    }
  ],
  "related_bills": [
    {
      "congress": "119",
      "context": "OTHER",
      "number": "47",
      "type": "SRES"
    }
  ]
}
```

## Schema Evolution

The schema is designed to be forward-compatible:

- **Required fields** should not be removed or changed
- **Optional fields** can be added without breaking existing code
- **Field types** should remain consistent
- **Enum values** (like `kind`) can be extended

When making changes to the schema:

1. Update the Pydantic models in `congressionalrecord/schema.py`
2. Run tests to ensure existing JSON files still validate
3. Update this documentation
4. Bump the package version appropriately

## Validation in CI/CD

To validate JSON output in automated workflows:

```bash
# Install dependencies
uv pip install pydantic

# Run validation on all output files
for file in output/**/*.json; do
    uv run python -c "
import json
from congressionalrecord.schema import CongressionalRecordDocument
with open('$file') as f:
    CongressionalRecordDocument(**json.load(f))
" || echo "Failed: $file"
done
```

## See Also

- [Pydantic Documentation](https://docs.pydantic.dev/)
- [JSON Schema Specification](https://json-schema.org/)
- [Congressional Record Parser Code](../congressionalrecord/govinfo/cr_parser.py)
