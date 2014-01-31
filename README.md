# Congressional Record

A parser for the Congressional Record.

---

## Supported sources

Currently only the GPO HTML packages are supported. 

Find files by date or download them from FDsys.

Urls look like this:
<http://www.gpo.gov/fdsys/pkg/CREC-2014-01-21.zip>
Download your own files and find `html` folder containing the pages of the day's record.


## Requirements

- lxml
- python 2.x

## Usage

(Make sure the x-bit is set on parser.py)

`./parser.py`

### Options

- `-id`, `--indir`: Input directory to parse. The.htm files in the dir will be processed. Front matter and other procedural text will not be processed.
- `-od`, `--outdir`: Output directory for parsed files. Defaults to __parsed in the input directory.
- `-l`, `--logdir`: Directory for logs to be written to. Defaults to __log in the input directory.
- '--interactive': Interactive mode: Step through files and choose which to parse.
- A positional argument can be provided with a single file to process, rather than iterating through a directory, but if `-id` is provided it will take precedence. Interactive mode is disabled when parsing a single file.

### Examples

Use --FindFileForMe with a day in yyyy-mm-dd format to extract records for that day.

Alternatively, find .htm files of the congressional record from [FDsys](http://www.gpo.gov/fdsys/browse/collection.action?collectionCode=CREC). When you find the day you are interested in, click on it and choose the "More" link. Then, download the Zip file. 

```
$ ./parser.py -h

usage: parser.py [-h] [-id INDIR] [-od OUTDIR] [-l LOGDIR] [--interactive]
                 [infile]

Parse arguments for the Congressional Record Parser

positional arguments:
  infile                The file to parse

optional arguments:
  -h, --help            show this help message and exit
  -id INDIR, --indir INDIR
                        An entire directory to traverse and parse, can replace
                        infile
  -od OUTDIR, --outdir OUTDIR
                        An output directory for the parsed content
  -l LOGDIR, --logdir LOGDIR
                        An output directory for logs
  --interactive         Step through files and decide whether or not to parse
                        each one
  -fffm, --FindFileForMe DATE
                        Choose a date (yyyy-mm-dd) to download and parse record. Files will be saved to the source folder.

$ ./parser.py -id ~/Projects/CR/CREC-2014-01-21/txt
flag status: False
saved file /Users/dan/Projects/CR/CREC-2014-01-21/txt/__parsed/CREC-2014-01-21-pt1-PgE109-2.xml to disk
flag status: False
saved file /Users/dan/Projects/CR/CREC-2014-01-21/txt/__parsed/CREC-2014-01-21-pt1-PgE109-3.xml to disk
flag status: False
saved file /Users/dan/Projects/CR/CREC-2014-01-21/txt/__parsed/CREC-2014-01-21-pt1-PgE109-4.xml to disk
...
```
