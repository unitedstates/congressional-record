[![Build Status](https://github.com/unitedstates/congressional-record/actions/workflows/ci.yml/badge.svg)](https://github.com/unitedstates/congressional-record/actions/workflows/ci.yml)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![code style: prettier](https://img.shields.io/badge/code_style-prettier-ff69b4.svg)](https://github.com/prettier/prettier)

# congressional-record

This tool converts HTML files containing the text of the Congressional Record into structured text data. It is particularly useful for identifying speeches by members of Congress.

From the repository root, type `python -m congressionalrecord.cli -h` for instructions.

- It outputs JSON
- Instances of speech are tagged with the speaker's bioguideid wherever possible
- Instances of speech are recorded as "turns," such that each subsequent instance of speech by a Member counts as a new "turn."

This software is released as-is under the BSD3 License, with no warranty of any kind.

# installation

Clone and download the repository:

```bash
git clone https://github.com/unitedstates/congressional-record.git
cd congressional-record
```

In Python 3 using `venv` for e.g.:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -e .
```

then `.venv/bin/python -m congressionalrecord.cli -h` to see usage instructions.


If using Python 3 with uv, use:

```bash
uv sync
```

then `uv run python -m congressionalrecord.cli -h` to see usage instructions.


# Recommended citation:

Judd, Nicholas, Dan Drinkard, Jeremy Carbaugh, and Lindsay Young. _congressional-record: A parser for the Congressional Record._ Chicago, IL: 2017.
