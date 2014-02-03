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

`./parse.py`

### Options
- A positional argument can be provided with a single date to process in YYYY-MM-DD format. It will look in the Source file to see if it has been downloaded, if not it will download the file from fdsys.
- '-f', '--infile': Input a singe file to process. If `-id` is provided it will take precedence. Interactive mode is disabled when parsing a single file.
- `-id`, `--indir`: Input directory to parse. Front matter and other procedural text will not be processed.
- `-od`, `--outdir`: Output directory for parsed files. Defaults to __parsed in the input directory.
- `-l`, `--logdir`: Directory for logs to be written to. Defaults to __log in the input directory.
- '--interactive': Interactive mode: Step through files and choose which to parse.

### Examples

Use parse.py and the day 

Alternatively, find .htm files of the congressional record from [FDsys](http://www.gpo.gov/fdsys/browse/collection.action?collectionCode=CREC). When you find the day you are interested in, click on it and choose the "More" link. Then, download the Zip file. 

```
$ ./parser.py -h

usage: parser.py [-h] [-id INDIR] [-od OUTDIR] [-l LOGDIR] [--interactive] [-f FILE]
                 [findfiles]

Parse arguments for the Congressional Record Parser

positional arguments:
  findfiles             Choose a date (yyyy-mm-dd) to download and parse record. 
                        Files will be saved to the source folder. If the records
                        already exist in the source folder, existing download will
                        be parsed again.

optional arguments:
  -h, --help            show this help message and exit
  -f, --infile          gives a particular file to parse
  -id INDIR, --indir INDIR
                        An entire directory to traverse and parse, can replace
                        infile
  -od OUTDIR, --outdir OUTDIR
                        An output directory for the parsed content
  -l LOGDIR, --logdir LOGDIR
                        An output directory for logs
  --interactive         Step through files and decide whether or not to parse
                        each one

$ ./parser.py -id ~/Projects/CR/CREC-2014-01-21/txt
flag status: False
saved file /Users/dan/Projects/CR/CREC-2014-01-21/txt/__parsed/CREC-2014-01-21-pt1-PgE109-2.xml to disk
flag status: False
saved file /Users/dan/Projects/CR/CREC-2014-01-21/txt/__parsed/CREC-2014-01-21-pt1-PgE109-3.xml to disk
flag status: False
saved file /Users/dan/Projects/CR/CREC-2014-01-21/txt/__parsed/CREC-2014-01-21-pt1-PgE109-4.xml to disk
...
```
