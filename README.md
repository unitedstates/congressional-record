# congressionalrecord2
*2015-07-25*

This is a fork of [the congressionalrecord repo](https://github.com/unitedstates/congressional-record), part of The United States Project and a product of The Sunlight Foundation and collaborators.

Like the original repo, it parses XML files downloaded from the Government Printing Office and produces structured text.

Unlike the original repo:
* It outputs JSON intended for use in ElasticSearch, not XML for Lucene.
* Instances of speech are tagged with the speaker's bioguideid wherever possible, leveraging new metadata not available when the parser was first written.
* The parser is rewritten to work on top of new libraries rather than with core and builtins. It might not be as fast, but the code is easier to read and modify.
* The parser is rewritten with certain other efficiency gains in mind -- for example, day-level metadata is parsed only once.

For now it has not been optimized for command line use and really works from the interpreter. It can:
* Produce a JSON version of any day of the Congressional Record, downloading new files if necessary
* Parse the Record and instead pass the resulting documents to an ElasticSearch cluster using bulk upload methods

**This is a radical departure from the original branch. The core ideas -- including the regex -- are from the original. All bugs are the mine.**

This software is released as-is under the MIT License, with no warranty of any kind.
