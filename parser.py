#!/usr/bin/env python

'''Parser for the plain text version of congressional record documents
   outputs the text marked up with xml
'''

import re
import datetime
import os
import sys
import argparse
import urllib2
from cStringIO import StringIO
from xml.sax.saxutils import escape, unescape

import lxml.etree

from fdsys.cr_parser import CRParser, parse_directory, parse_single


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Parse arguments for the Congressional Record Parser")
    parser.add_argument('infile', type=str, nargs='?',
                        help='The file to parse')
    parser.add_argument('-id', '--indir', dest='indir', action='store',
                        help='An entire directory to traverse and parse, can replace infile')
    parser.add_argument('-od', '--outdir', dest='outdir', action='store',
                        help='An output directory for the parsed content')
    parser.add_argument('-l', '--logdir', dest='logdir', action='store',
                        help='An output directory for logs')
    parser.add_argument('--interactive', dest='interactive', action='store_true',
                        help='Step through files and decide whether or not to parse each one')
    args = parser.parse_args()

    # Deal with directory case:
    if args.indir:
        if not args.logdir:
            args.logdir = os.path.realpath(os.path.join(args.indir, '__log'))
        if not args.outdir:
            args.outdir = os.path.realpath(os.path.join(args.indir, '__parsed'))
        parse_directory(args.indir, interactive=args.interactive,
                        logdir=args.logdir, outdir=args.outdir)
    # Deal with single file case:
    elif args.infile:
        if not args.logdir:
            args.logdir = os.path.realpath(os.path.join(os.path.dirname(args.infile), '__log'))
        if not args.outdir:
            args.outdir = os.path.realpath(os.path.join(os.path.dirname(args.infile), '__parsed'))
        parse_single(args.infile, logdir=args.logdir, outdir=args.outdir)
    else:
        parser.print_help()
        raise 'Either an infile argument or the --indir flag is required!'
