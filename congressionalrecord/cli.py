#!/usr/bin/env python
import os
import sys
from pg_run.pg_cr_bulkwrite import crToPG as cr
from fdsys.downloader import Downloader as dl
import argparse

def main():
    parser = argparse.ArgumentParser(
        prog="cr2 test",
        description="Test the argparser")

    parser.add_argument(
        'start', type=str,
        help='The day or first day of Record text \
        user wants to download.')

    parser.add_argument(
        'end', type=str,
        help='The last day in a contiguous series of days \
        user wants to download. Note the parser skips \
        days with no activity.')

    parser.add_argument(
        'do_mode',
        type=str,
        choices=['json','es','pg','noparse'],
        help='json: Store json\n \
        es: Push to ElasticSearch.\n \
        pg: Generate flatfiles for Postgres.\n \
        noparse: Just download the files.')

    parser.add_argument(
        '--index',
        type=str,
        help='If using elasticsearch, this is the index to use.')

    parser.add_argument(
        '--es_url',
        type=str,
        help='If using elasticsearch, this is the URL of the\
        elasticsearch cluster.')

        
    args = parser.parse_args()

    if args.do_mode == 'pg':
        cr(args.start,end=args.end,do_mode='yield')
    else:
        print "Haven't written the hooks for other functionality yet."

    
if __name__ == '__main__':
    main()
