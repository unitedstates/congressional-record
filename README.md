# Congressional Record

This tool uses the Sunlight Foundation's [Capitol Words](https://github.com/sunlightlabs/Capitol-Words) parser to mark up the Congressional record in XML. 

## Supported sources

Find files by date, or download them from [FDsys](http://www.gpo.gov/fdsys/browse/collection.action?collectionCode=CREC). 

Currently only the GPO HTML packages are supported. 

FDsys URLs look like this: `http://www.gpo.gov/fdsys/pkg/CREC-2014-01-21.zip`

Download your own files and find the `html` folder containing the pages of the day's record.

Be aware that there is a usage limit on FDsys downloads per day. If you exceed the limit, your IP will be blocked from downloading for a period of time. 


## Requirements

- lxml
- Python 2.7.x

## Usage

`parsecr [YYYY-MM-DD]`

### Options
- A positional argument for dates, in `YYYY-MM-DD` format. This can be a single date, a list of dates, or a range of dates. Date ranges should be given as start date, then end date, e.g. `YYYY-MM-DD:YYYY-MM-DD`. For several specific days, put a space between each date. The parser will look for a previous file to see if it has been downloaded. If not, it will download the file from FDsys.
- `-f`, `--infile`: Input a single file to process. If `-id` is provided, it will take precedence. Interactive mode is disabled when parsing a single file.
- `-id`, `--indir`: Input directory to parse. Front matter and other procedural text will not be processed.
- `-od`, `--outdir`: Output directory for parsed files. Defaults to `__parsed` in the input directory.
- `-l`, `--logdir`: Directory for logs to be written to. Defaults to `__log` in the input directory.
- `--interactive`: Interactive mode: Step through files and choose which to parse.


### Examples

In this example, the parsed XML records would appear in a folder named `congressional-record/source/2014/CREC-2014-01-27/__parsed/`. The output is shortened:

```
$ parsecr 2014-01-30 
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

Alternatively, find .htm files of the Congressional Record from [FDsys](http://www.gpo.gov/fdsys/browse/collection.action?collectionCode=CREC). When you find the day you are interested in, click on it and choose the "More" link. Then, download the zip file and use the `-id` flag to point to the htm files. 

```
$ parsecr -h

usage: parsecr [-h] [-f INFILE] [-id INDIR] [-od OUTDIR] [-l LOGDIR]
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
