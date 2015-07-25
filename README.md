# congressionalrecord2
*2015-07-25*

This is a fork of [the congressionalrecord repo](https://github.com/unitedstates/congressional-record), part of The United States Project and a product of The Sunlight Foundation and collaborators.

Like the original repo, it parses XML files downloaded from the Government Printing Office and produces structured text.

Unlike the original repo:
* It outputs JSON intended for use in ElasticSearch, not XML for Lucene.
* Instances of speech are tagged with the speaker's bioguideid wherever possible, leveraging new metadata not available when the parser was first written.
* The parser is rewritten to work on top of new libraries rather than with core and builtins. It might not be as fast, but the code is easier to read and modify.
* The parser is rewritten with certain other efficiency gains in mind -- for example, day-level metadata is parsed only once.
* Instances of speech are recorded as "turns," such that each subsequent instance of speech by a Member counts as a new "turn." (Computational linguists: You're welcome.)

For now it has not been optimized for command line use and really works from the interpreter. It can:
* Produce a JSON version of any day of the Congressional Record, downloading new files if necessary
* Parse the Record and instead pass the resulting documents to an ElasticSearch cluster using bulk upload methods

It has weaknesses:
* Bill text, letters and other material read into the Record, roll call votes and other things that are not members of Congress speaking are included, but misclassified -- portions are tagged are "titles" or "line breaks."

But also strengths:
* This parser's approach dramatically reduces the amount of material mistakenly included under a member of Congress' name. Currently the cruft is limited to the occasional note from the Recorder (such as "(Ms. SO-AND-SO asked for and was given permission to ...)") and page numbers (Like [[Page S5678]] that are sometimes not caught.

**This is a radical departure from the original branch. The core ideas -- including the regex -- are from the original. All bugs are the mine.**

This software is released as-is under the BSD3 License, with no warranty of any kind.
