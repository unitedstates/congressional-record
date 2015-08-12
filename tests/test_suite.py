import unittest
from congressionalrecord.fdsys import cr_parser as cr
from congressionalrecord.fdsys import downloader as dl
import random
import os
from datetime import datetime,timedelta
import json
import re
import logging

logging.basicConfig(filename='unittests.log',level=logging.DEBUG)

class testCRDir(unittest.TestCase):
    def test(self):
        """
        CRDir pointed at correct path
        """
        input_string = 'output/2005/CREC-2005-07-20'
        crdir = cr.ParseCRDir(input_string)
        self.assertEqual(crdir.cr_dir,input_string)

class testCRFile(unittest.TestCase):
    def setUp(self):
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
        self.assertEqual(download.status,downloadFailure)

    def test_handle_existing(self):
        download = dl.Downloader('2005-07-20')
        self.assertEqual(download.status,'existingFiles')
        
class testJson(unittest.TestCase):

    def setUp(self):
        startd = datetime(2005,1,1)
        lastd = datetime(2015,7,31)
        duration = lastd - startd
        ndays = random.randint(0,duration.days)
        testd = startd + timedelta(ndays)
        self.download_day = datetime.strftime(testd,'%Y-%m-%d')
        self.download_year = str(testd.year)

    def test_no_text_in_line_breaks(self):
        d = dl.Downloader(self.download_day,do_mode='json')
        rootdir = os.path.join('output',self.download_year)
        for root,dirs,files in os.walk('output'):
            if 'json' in dirs:
                for afile in os.listdir(os.path.join(root,'json')):
                    fp = os.path.join(root,'json',afile)
                    logging.info('Into file:\n\t{0}'.format(fp))
                    with open(fp,'r') as raw:
                        testf = json.load(raw)                    
                    for item in testf['content']:
                        if item['kind'] == 'linebreak':
                            for line in item['text'].split('\n'):
                                self.assertFalse(
                                    re.match(r".*[a-zA-Z]+",line))
