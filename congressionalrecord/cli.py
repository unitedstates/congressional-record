#!/usr/bin/env python

'''Parser for the plain text version of congressional record documents
   outputs the text marked up with xml
'''

import datetime
import os
import argparse

from .fdsys.cr_parser import parse_directory, parse_single
from .fdsys.simple_scrape import find_fdsys


def daterange(start, end, date_format=None):
    delta = end - start
    for i in range(abs(delta.days) + 1):
        date = start + datetime.timedelta(days=i)
        if date_format:
            date = datetime.datetime.strftime(date, date_format)
        yield date


def parsedate(s):
    return datetime.datetime.strptime(s.strip(), "%Y-%m-%d")


def main():
    default_outdir = os.path.join(os.getcwd(), 'output')

    parser = argparse.ArgumentParser(
        prog="parsecr",
        description="Parse arguments for the Congressional Record Parser")

    parser.add_argument('days', type=str, nargs='*',
                        help='A positional argument for dates. This can be a single date, a list \
                        of dates or a range of dates. Records will be  Make sure dates are in \
                        YYYY-MM-DD format. Date ranges should be given as start date then end \
                        date YYYY-MM-DD:YYYY-MM-DD. For several specific days, write out the \
                        dates in the correct format with a space between each date.\n\
                        The parser will look for a previous file to see if it has been downloaded, \
                        if not, it will download the file from fdsys.')

    parser.add_argument('-f', '--infile', dest='infile', action='store',
                        help='Parse a single txt or htm file.')
    parser.add_argument('-id', '--indir', dest='indir', action='store',
                        help='An entire directory to traverse and parse, can replace infile')
    parser.add_argument('-od', '--outdir', dest='outdir', action='store',
                        help='An output directory for the parsed content')
    parser.add_argument('-l', '--logdir', dest='logdir', action='store',
                        help='An output directory for logs')
    parser.add_argument('--interactive', dest='interactive', action='store_true',
                        help='Step through files and decide whether or not to parse each one')
    parser.add_argument('--force', dest='force', action='store_true',
                        help='Force documents to be downloaded id the txt files already exist.')
    parser.add_argument('--ntf', '-no_text_files', dest='notext', action='store_true',
                        help='Remove the text version of the documents.(The .htm version is automatically removed)\
                        EVERYING in the indir folder will be removed.')

    args = parser.parse_args()

    # Scrapes files and creates a directory from FDsys if no file exists in source folder
    if args.days:

        if not args.outdir:
            args.outdir = default_outdir

        no_record = []
        dates = []

        for date_arg in args.days:
            if ':' in date_arg:
                start_end = date_arg.split(':')
                if len(start_end) == 1:
                    dates.append(date_range)
                else:
                    begin = parsedate(start_end[0])
                    end = parsedate(start_end[1])
                    dates.extend(daterange(begin, end, "%Y-%m-%d"))
            else:
                dates.append(date_arg)

        for day in dates:
            doc_path = find_fdsys(day, force=args.force, outdir=args.outdir)

            # did not return records
            if doc_path is None:
                no_record.append(day)

            else:
                file_path = os.path.dirname(doc_path)
                if not args.logdir:
                    args.logdir = os.path.realpath(os.path.join(file_path, '__log'))
                parsed_path = os.path.realpath(os.path.join(file_path, '__parsed'))
                parse_directory(doc_path, interactive=args.interactive,
                                logdir=args.logdir, outdir=parsed_path)
            if args.notext:
                for filename in os.listdir(doc_path):
                    if filename.endswith('.txt') or filename.endswith('.xml') or filename.endswith('.htm'):
                        file_path = os.path.join(doc_path, filename)
                        os.remove(file_path)
                os.rmdir(doc_path)

        if len(no_record) > 0:
            print "No results were found for the following day/s: %s " % (no_record)

    # Deal with directory case:
    elif args.indir:
        if not args.logdir:
            args.logdir = os.path.realpath(os.path.join(args.indir, '__log'))
        if not args.outdir:
            args.outdir = os.path.realpath(os.path.join(args.indir, '__parsed'))
        parse_directory(args.indir, interactive=args.interactive,
                        logdir=args.logdir, outdir=args.outdir)
        if args.notext:
            for filename in os.listdir(doc_path):
                if filename.endswith('.txt') or filename.endswith('.xml') or filename.endswith('.htm'):
                    file_path = os.path.join(doc_path, filename)
                    os.remove(file_path)
            os.rmdir(doc_path)

    # Deal with single file case:
    elif args.infile:
        if not args.logdir:
            args.logdir = os.path.realpath(os.path.join(os.path.dirname(args.infile), '__log'))
        if not args.outdir:
            args.outdir = os.path.realpath(os.path.join(os.path.dirname(args.infile), '__parsed'))
        parse_single(args.infile, logdir=args.logdir, outdir=args.outdir)

        if args.notext:
            os.remove(args.infile)

    else:
        msg = 'Either a date (YYYY-MM-DD), --infile argument or the --indir flag is required!'
        parser.error(msg)


if __name__ == '__main__':
    main()
