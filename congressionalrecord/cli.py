#!/usr/bin/env python
from __future__ import absolute_import, print_function

import argparse
import logging

from .govinfo.downloader import Downloader as dl
from .pg_run.pg_cr_bulkwrite import crToPG as cr


def main():
    parser = argparse.ArgumentParser(
        description="Download and parse the text of the \
        Congressional Record."
    )

    parser.add_argument(
        "start",
        type=str,
        help="The day or first day of Record text \
        user wants to download. (Format: YYYY-MM-DD)",
    )

    parser.add_argument(
        "end",
        type=str,
        help="The last day in a contiguous series of days \
        user wants to download. Note the parser skips \
        days with no activity. (Format: YYYY-MM-DD)",
    )

    parser.add_argument(
        "do_mode",
        type=str,
        choices=["json", "pg", "noparse"],
        help="json: Store json\n \
        pg: Generate flatfiles for Postgres.\n \
        noparse: Just download the files.",
    )

    parser.add_argument(
        "--csvpath", type=str, help="Optional path for csv files if using pg do_mode."
    )

    parser.add_argument(
        "--logfile", type=str, help="Use a particular logfile.", default="cr2.log"
    )

    args = parser.parse_args()
    logging.basicConfig(filename=args.logfile, level=logging.DEBUG)
    logging.info("Logging begins")
    if args.csvpath and args.do_mode == "pg":
        cr(args.start, end=args.end, do_mode="yield", csvpath=args.csvpath)
    elif args.do_mode == "pg":
        cr(args.start, end=args.end, do_mode="yield")
    elif args.do_mode == "json":
        dl(args.start, end=args.end, do_mode="json")
    else:
        print("Haven't written the hooks for other functionality yet.")

    logging.info("Logging ends")


if __name__ == "__main__":
    main()
