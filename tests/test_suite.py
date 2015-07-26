import unittest
from congressionalrecord.fdsys import downloader as dl
from datetime import datetime,timedelta
import random
import json
import os

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
        download = dl.Downloader(pick_a_day,do_mode='json')
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
        download = dl.Downloader(self.day,do_mode='json',outpath='congressionalrecord/tests/output')
        while download.status == 404:
            self.day = self.pick_a_day()
            download = dl.Downloader(self.day,do_mode='json',outpath='congressionalrecord/tests/output')

    def test(self):
        """
        Success case: JSON has all the fields we expect,
        plus some content
        """
        year = datetime.strptime(self.day,'%Y-%m-%d').year()
        crec_path = 'CREC-' + self.day
        adir = 'congressionalrecord/tests/output/{0}/{1}/json'.format(year,crec_path)
        ran_file = os.path.join(adir,random.choice(os.listdir(adir)))
        with open(ran_file,'r') as infile:
            some_json = json.load(infile)

        # All the keys are there
        for key in ['content','header','id','title']:
            self.assertTrue(key in some_json.keys(),msg='{0} not in keys!'.format(key))

        # Content is not empty
        self.assertGreater(len(some_json['content']),0,msg='Content empty')

        # Can construct a valid date from date fields
        date_field = some_json['header']['year'] + '-' + some_json['header']['month'] + '-' + some_json['header']['day']
        self.assertTrue(type(datetime.strptime(date_field,'%Y-%b-%d')) == datetime,msg='Cannot construct valid date.')


        
        
        
