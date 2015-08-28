import unittest
from congressionalrecord.fdsys import cr_parser as cr
from congressionalrecord.fdsys import downloader as dl
import random
import os
from datetime import datetime,timedelta
import json
import re
import logging

logging.basicConfig(filename='tests.log',level=logging.DEBUG)

class testCRDir(unittest.TestCase):

    def setUp(self):
        download = dl.Downloader('2005-07-20',do_mode='json')

    def test(self):
        """
        CRDir pointed at correct path
        """
        input_string = 'output/2005/CREC-2005-07-20'
        crdir = cr.ParseCRDir(input_string)
        self.assertEqual(crdir.cr_dir,input_string)

class testCRFile(unittest.TestCase):
    def setUp(self):
        download = dl.Downloader('2005-07-20',do_mode='json')
        input_string = 'output/2005/CREC-2005-07-20'
        self.crdir = cr.ParseCRDir(input_string)
        input_dir = os.path.join(input_string,'html')
        input_file = random.choice(os.listdir(input_dir))
        self.input_path = os.path.join(input_dir,input_file)

    def test_top_level_keys(self):
        """
        CRFile has all the right fixins' in the crdoc
        """
        crfile = cr.ParseCRFile(self.input_path,self.crdir)
        for x in ['doc_title','header','content','id']:
            self.assertIn(x,crfile.crdoc.keys(),msg='{0} not in crdoc!'.format(x))

    def test_content_length(self):
        crfile = cr.ParseCRFile(self.input_path,self.crdir)
        self.assertGreater(crfile.crdoc['content'],0,msg='No items in content!')

class testDownloader(unittest.TestCase):

    def test_handle_404(self):
        download = dl.Downloader('2015-07-19',do_mode='json')
        self.assertEqual(download.status,'downloadFailure')

    def test_handle_existing(self):
        download = dl.Downloader('2005-07-20',do_mode='json')
        self.assertIn(download.status,['extractedFilesdeletedZip','existingFiles'])

class testLineBreak(unittest.TestCase):

    def setUp(self):
        d = dl.Downloader('2014-11-19',do_mode='json')
        self.sp = re.compile(r'^(\s{1,2}|<bullet>)(?P<name>((((Mr)|(Ms)|(Mrs)|(Miss))\. (([-A-Z\'])(\s)?)+( of [A-Z][a-z]+)?)|((The ((VICE|ACTING|Acting) )?(PRESIDENT|SPEAKER|CHAIR(MAN)?)( pro tempore)?)|(The PRESIDING OFFICER)|(The CLERK)|(The CHIEF JUSTICE)|(The VICE PRESIDENT)|(Mr\. Counsel [A-Z]+))( \([A-Za-z.\- ]+\))?))\.')

    def test_fixedLineBreak(self):
        rootdir = 'output/2014/CREC-2014-11-19/json'
        for apath in os.listdir(rootdir):
            thepath = os.path.join(rootdir,apath)
            with open(thepath,'r') as thefile:
                thejson = json.load(thefile)
            for item in thejson['content']:
                if item['kind'] != 'speech':
                    for line in item['text'].split('\n'):
                        self.assertFalse(
                            self.sp.match(line),
                            'Check {0}'.format(apath))

            
class testJson(unittest.TestCase):

    def setUp(self):
        startd = datetime(2013,1,1)
        lastd = datetime(2015,7,31)
        duration = lastd - startd
        ndays = random.randint(0,duration.days)
        testd = startd + timedelta(ndays)
        self.download_day = datetime.strftime(testd,'%Y-%m-%d')
        self.download_year = str(testd.year)
        self.sp = re.compile(r'^(\s{1,2}|<bullet>)(?P<name>((((Mr)|(Ms)|(Mrs)|(Miss))\. (([-A-Z\'])(\s)?)+( of [A-Z][a-z]+)?)|((The ((VICE|ACTING|Acting) )?(PRESIDENT|SPEAKER|CHAIR(MAN)?)( pro tempore)?)|(The PRESIDING OFFICER)|(The CLERK)|(The CHIEF JUSTICE)|(The VICE PRESIDENT)|(Mr\. Counsel [A-Z]+))( \([A-Za-z.\- ]+\))?))\.')
        d = dl.Downloader(self.download_day,do_mode='json')
        while d.status == 'downloadFailure':
            ndays = random.randint(0,duration.days)
            testd = startd + timedelta(ndays)
            self.download_day = datetime.strftime(testd,'%Y-%m-%d')
            self.download_year = str(testd.year)
            d = dl.Downloader(self.download_day,do_mode='json')

    def test_noSpeakersOutsideSpeech_Fresh(self):
        rootdir = os.path.join('output',self.download_year,'CREC-'+self.download_day,'json')
        for afile in os.listdir(rootdir):
            apath = os.path.join(rootdir,afile)
            logging.info('loading {0}'.format(apath))
            with open(apath, 'r') as inson:
                testf = json.load(inson)
                for item in testf['content']:
                    if item['kind'] != 'speech':
                        for line in item['text'].split('\n'):
                            self.assertFalse(
                                self.sp.match(line),
                                'Check {0}'.format(apath))

    def test_noSpeakersOutsideSpeech_All(self):
        for root,dirs,files in os.walk('output'):
            if 'json' in root:
                for afile in files:
                    apath = os.path.join(root,afile)
                    logging.info('loading {0}'.format(apath))
                    with open(apath, 'r') as inson:
                        testf = json.load(inson)
                    for item in testf['content']:
                        if item['kind'] != 'speech':
                            for line in item['text'].split('\n'):
                                self.assertFalse(
                                    self.sp.match(line),
                                    'Check {0}'.format(apath))

    def test_noTextInLineBreaks_Fresh(self):
        rootdir = os.path.join('output',self.download_year,'CREC-'+self.download_day,'json')
        for afile in os.listdir(rootdir):
            apath = os.path.join(rootdir,afile)
            logging.info('loading {0}'.format(apath))
            with open(apath, 'r') as inson:
                testf = json.load(inson)
                for item in testf['content']:
                    if item['kind'] == 'linebreak':
                        for line in item['text'].split('\n'):
                            self.assertFalse(
                                re.match(r"\s*[a-zA-Z]+",line),
                                'Check {0}'.format(apath))
