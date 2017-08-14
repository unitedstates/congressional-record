[![Build Status](https://travis-ci.org/nclarkjudd/congressionalrecord2.png)](https://travis-ci.org/nclarkjudd/congressionalrecord2)
# congressionalrecord2
*2015-07-25*

This is a fork of [the congressionalrecord repo](https://github.com/unitedstates/congressional-record), part of The United States Project and a product of The Sunlight Foundation and collaborators.

Like the original, it parses XML files downloaded from the Government Printing Office and produces structured text.

This version has a command line interface and is under heavy development. From the repository root, type ``python -m congressionalrecord.cli -h`` for instructions.

Unlike the original repo:
* It outputs JSON intended for use in ElasticSearch, not XML for Lucene.
* Instances of speech are tagged with the speaker's bioguideid wherever possible, leveraging new metadata not available when the parser was first written.
* The parser is rewritten to work on top of new libraries rather than with core and builtins. It might not be as fast, but the code is easier to read and modify.
* The parser is rewritten with certain other efficiency gains in mind -- for example, day-level metadata is parsed only once.
* Instances of speech are recorded as "turns," such that each subsequent instance of speech by a Member counts as a new "turn." 

This software is released as-is under the BSD3 License, with no warranty of any kind.

# Recommended citation:

Judd, Nicholas, Dan Drinkard, Jeremy Carbaugh, and Lindsay Young. *congressional-record: A parser for the Congressional Record.* Chicago, IL: 2017.
