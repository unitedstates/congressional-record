[![Build Status](https://travis-ci.org/unitedstates/congressional-record.png)](https://travis-ci.org/unitedstates/congressional-record)

# congressional-record

This tool converts HTML files containing the text of the Congressional Record into structured text data. It is particularly useful for identifying speeches by members of Congress.

From the repository root, type ``python -m congressionalrecord.cli -h`` for instructions.

* It outputs JSON
* Instances of speech are tagged with the speaker's bioguideid wherever possible
* Instances of speech are recorded as "turns," such that each subsequent instance of speech by a Member counts as a new "turn." 

This software is released as-is under the BSD3 License, with no warranty of any kind.

# installation

In Python 3 using `venv` for e.g.:

```
git clone https://github.com/unitedstates/congressional-record.git
cd congressional-record
python3 -m venv .venv
.venv/bin/python -m pip install -e .
```

then `.venv/bin/python -m congressionalrecord.cli -h` to see usage instructions.

# Recommended citation:

Judd, Nicholas, Dan Drinkard, Jeremy Carbaugh, and Lindsay Young. *congressional-record: A parser for the Congressional Record.* Chicago, IL: 2017.
