import unittest
from congressionalrecord.fdsys import downloader as dl
from datetime import datetime,timedelta
import random
import json
import os
import sys

"""
These are chaosmonkey style tests! They work with LIVE DATA.
So if it happens upon a year/day that has already been populated, the
JSON for that day is repopulated.

If the output isn't there already, it is downloaded.

The tests going forward should be a mix of big integration tests (as in the
first tests) as well as more traditional narrowbore unit tests.
"""

class testDownloader(unittest.TestCase):
    """
    Should be able to download an arbitrary day of Record text,
    parse, and output JSON with no problems.
    """
    def pick_a_day(self):
        today = datetime.today().date()
        earliest_day = datetime(1994,1,25).date()
        duration = today - earliest_day
        chosen_day = random.randrange(0,duration.days)
        chosen_date = earliest_day + timedelta(days=chosen_day)
        datestr = datetime.strftime(chosen_date,"%Y-%m-%d")
        return datestr

    def test(self):
        """
        Success case:
        Downloader reports one of two anticipated status codes:
        True or 404
        """
        day = self.pick_a_day()
        download = dl.Downloader(day,do_mode='json',outpath='output')
        self.assertIn(download.status,[404,True],msg='Unexpected status {0}'.format(download.status))

class testJSONValidity(testDownloader):
    """
    An arbitrary page of JSON from an arbitrary day
    has all of the fields we want it to have.

    It's not cheating to pull a day for ourselves that
    definitely has content.
    """

    def setUp(self):
        print('In setUp()')
        self.day = self.pick_a_day()
        self.download = dl.Downloader(self.day,do_mode='json',outpath='output')
        while self.download.status == 404:
            self.day = self.pick_a_day()
            self.download = dl.Downloader(self.day,do_mode='json',outpath='output')

    def test(self):
        """
        Success case: JSON has all the fields we expect,
        plus some content
        """
        year = datetime.strptime(self.day,'%Y-%m-%d').year
        crec_path = 'CREC-' + self.day
        adir = 'output/{0}/{1}/json'.format(year,crec_path)
        ran_file = os.path.join(adir,random.choice(os.listdir(adir)))
        with open(ran_file,'r') as infile:
            self.some_json = json.load(infile)

        # All the keys are there
        for key in ['content','header','id','title']:
            self.assertTrue(key in self.some_json.keys(),msg='{0} not in keys!'.format(key))

class testJSONHasContent(testJSONValidity):

    def test(self):
        """
        Success case: JSON has content
        """
        year = datetime.strptime(self.day,'%Y-%m-%d').year
        crec_path = 'CREC-' + self.day
        adir = 'output/{0}/{1}/json'.format(year,crec_path)
        ran_file = os.path.join(adir,random.choice(os.listdir(adir)))
        with open(ran_file,'r') as infile:
            self.some_json = json.load(infile)
        # Content is not empty
        self.assertGreater(len(self.some_json['content']),0,msg='Content empty')

class testJSONHasValidDate(testJSONValidity):

    def test(self):
        """
        Success case: JSON includes valid date field
        """
        year = datetime.strptime(self.day,'%Y-%m-%d').year
        crec_path = 'CREC-' + self.day
        adir = 'output/{0}/{1}/json'.format(year,crec_path)
        ran_file = os.path.join(adir,random.choice(os.listdir(adir)))
        with open(ran_file,'r') as infile:
            self.some_json = json.load(infile)

        # Can construct a valid date from date fields
        date_field = self.some_json['header']['year'] + '-' + self.some_json['header']['month'] + '-' + self.some_json['header']['day']
        self.assertTrue(type(datetime.strptime(date_field,'%Y-%B-%d')) == datetime,msg='Cannot construct valid date.')
