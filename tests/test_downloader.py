import unittest
from congressionalrecord.govinfo import cr_parser as cr
from congressionalrecord.govinfo import downloader as dl
import random
import os
from datetime import datetime,timedelta
import json
import re
import logging

logging.basicConfig(filename='tests.log',level=logging.DEBUG)

class testDownloader(unittest.TestCase):

    def test_handle_404(self):
        download = dl.Downloader('2015-07-19',do_mode='json')
        self.assertEqual(download.status,'downloadFailure')

    def test_handle_existing(self):
        download = dl.Downloader('2005-07-20',do_mode='json')
        self.assertIn(download.status,['extractedFilesdeletedZip','existingFiles'])

    def test_handle_empty(self):
        download = dl.Downloader('2017-01-02',do_mode='json')
        self.assertEqual(download.status,'downloadFailure')
