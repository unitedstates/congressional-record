import unittest
from congressionalrecord.fdsys import cr_parser as cr
from congressionalrecord.fdsys import downloader as dl
import random
import os
from datetime import datetime,timedelta
import json
import re

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

    def handle_404(self):
        download = dl.Downloader('2015-07-19',do_mode='json')
        self.assertEqual(download.status,404)

    def handle_existing(self):
        download = dl.Downloader('2005-07-20')
        self.assertEqual(download.status,'existingFiles')
        
class testJson(unittest.TestCase):

    def setUp(self):
        startd = datetime(2005,1,1)
        lastd = datetime(2015,7,31)
        duration = lastd - startd
        ndays = random.randint(0,duration)
        testd = startd + timedelta(ndays)
        self.download_day = datetime.strftime(testd,'%Y-%m-%d')
        self.download_year = datetime.strftime(testd,'%Y-%m-%d').year

    def noTextInLineBreaks(self):
        d = dl.Downloader(self.download_day,do_mode='json')
        rootdir = os.path.join('output',self.download_year)
        n_checked = 0
        for root,dirs,files in os.path.walk(rootdir):
            if root == 'json':
                for afile in files:
                    testf = json.load(afile)
                    for item in testf['content']:
                        if item['kind'] == 'linebreak':
                            for line in item['text'].split('\n'):
                                self.assertFalse(
                                    re.match(r".*[\w]+",line))
                                
    def noTextInLineBreaksAtAll(self):
        for root,dirs,files in os.path.walk('output'):
            if root == 'json':
                for afile in files:
                    testf = json.load(afile)
                    for item in testf['content']:
                        for line in item['text'].split('\n'):
                            self.assertFalse(
                                re.match(r".*[\w]+",line))
    

    

        
