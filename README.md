# Congressional Record

This tool uses the Sunlight Foundation's [Capitol Words](https://github.com/sunlightlabs/Capitol-Words) parser to markup the Congressional record in xml. 

---

## Supported sources

Find files by date or download them from [FDsys](http://www.gpo.gov/fdsys/browse/collection.action?collectionCode=CREC). 

Currently only the GPO HTML packages are supported. 

FDsys urls look like this:
<http://www.gpo.gov/fdsys/pkg/CREC-2014-01-21.zip>
Download your own files and find `html` folder containing the pages of the day's record.

Be aware that there is a usage limit on the FDsys download per day. If you exceed the limit, your ip will be blocked from downloading for a period of time. 


## Requirements

- lxml
- python 2.x

## Usage

(Make sure the x-bit is set on parser.py)

`./parsecr.py`

### Options
- A positional argument for dates. This can be a single date, a list
  of dates or a range of dates. Records will be  Make sure dates are in
  YYYY-MM-DD format. Date ranges should be given as start date then end 
  date YYYY-MM-DD:YYYY-MM-DD. For several specific days, write out the 
  dates in the correct format with a space between each date.
  The parser will look for a previous file to see if it has been downloaded, 
  if not, it will download the file from fdsys.
- '-f', '--infile': Input a singe file to process. If `-id` is provided it will take precedence. Interactive mode is disabled when parsing a single file.
- `-id`, `--indir`: Input directory to parse. Front matter and other procedural text will not be processed.
- `-od`, `--outdir`: Output directory for parsed files. Defaults to __parsed in the input directory.
- `-l`, `--logdir`: Directory for logs to be written to. Defaults to __log in the input directory.
- '--interactive': Interactive mode: Step through files and choose which to parse.


### Examples

Use parsecr.py and a date in YYYY-MM-DD format or look for a date range with the beginning date directly followed by a slash and the end date YYYY-MM-DD:YYYY-MM-DD.

The output shortened in the following example. In this example, he parsed xml records would appear in the folder named /congressional-record/source/2014/CREC-2014-01-27/__parsed/

```
$ ./parsecr.py 2014-01-30 
Downloading url  http://www.gpo.gov/fdsys/pkg/CREC-2014-01-27.zip
Processing  CREC-2014-01-27/html/CREC-2014-01-27-pt1-PgD73-2.htm
Processing  CREC-2014-01-27/html/CREC-2014-01-27-pt1-PgD73.htm
Processing  CREC-2014-01-27/html/CREC-2014-01-27-pt1-PgD74-2.htm
 ...
 CREC-2014-01-27-pt1-PgE115-2.htm
source/2014/CREC-2014-01-27
flag status: False
saved file congressional-record/source/2014/CREC-2014-01-27/__parsed/CREC-2014-01-27-pt1-PgE115-2.xml to disk
CREC-2014-01-27-pt1-PgE115-3.htm
source/2014/CREC-2014-01-27
flag status: False
saved file congressional-record/source/2014/CREC-2014-01-27/__parsed/CREC-2014-01-27-pt1-PgE115-3.xml to disk
 ... 

```

Alternatively, find .htm files of the congressional record from [FDsys](http://www.gpo.gov/fdsys/browse/collection.action?collectionCode=CREC). When you find the day you are interested in, click on it and choose the "More" link. Then, download the Zip file and use the -id command to point to the htm files. 

```
$ ./parser.py -h

usage: parsecr.py [-h] [-f INFILE] [-id INDIR] [-od OUTDIR] [-l LOGDIR]
                [--interactive] [--force] [--ntf]
                [days [days ...]]

Parse arguments for the Congressional Record Parser

positional arguments:
  days                  A positional argument for dates. This can be a single
                        date, a list of dates or a range of dates. Records
                        will be Make sure dates are in YYYY-MM-DD format. Date
                        ranges should be given as start date then end date
                        YYYY-MM-DD:YYYY-MM-DD. For several specific days,
                        write out the dates in the correct format with a space
                        between each date. The parser will look for a previous
                        file to see if it has been downloaded, if not, it will
                        download the file from fdsys.

optional arguments:
  -h, --help            show this help message and exit
  -f INFILE, --infile INFILE
                        Parse a single txt or htm file.
  -id INDIR, --indir INDIR
                        An entire directory to traverse and parse, can replace
                        infile
  -od OUTDIR, --outdir OUTDIR
                        An output directory for the parsed content
  -l LOGDIR, --logdir LOGDIR
                        An output directory for logs
  --interactive         Step through files and decide whether or not to parse
                        each one
  --force               Force documents to be downloaded id the txt files
                        already exist.


$ ./parser.py -id ~/Projects/CR/CREC-2014-01-21/txt
flag status: False
saved file /Users/dan/Projects/CR/CREC-2014-01-21/txt/__parsed/CREC-2014-01-21-pt1-PgE109-2.xml to disk
flag status: False
saved file /Users/dan/Projects/CR/CREC-2014-01-21/txt/__parsed/CREC-2014-01-21-pt1-PgE109-3.xml to disk
flag status: False
saved file /Users/dan/Projects/CR/CREC-2014-01-21/txt/__parsed/CREC-2014-01-21-pt1-PgE109-4.xml to disk
...
```
