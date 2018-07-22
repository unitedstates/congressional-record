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

"""
These tests make sure that basic parser functions
run as expected, generating files full of JSON output
such that nothing that looks like
a speech exists outside of a "speech" JSON item.
"""

class testCRDir(unittest.TestCase):

    def setUp(self):
        pass

    def test_crdir(self):
        """
        CRDir pointed at correct path
        """
        input_string = 'tests/test_files/CREC-2005-07-20'
        crdir = cr.ParseCRDir(input_string)
        self.assertEqual(crdir.cr_dir,input_string)

class testCRFile(unittest.TestCase):

    def setUp(self):
        input_string = 'tests/test_files/CREC-2005-07-20'
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
        self.assertGreater(len(crfile.crdoc['content']),0,msg='No items in content!')

class testLineBreak(unittest.TestCase):

    def setUp(self):
        self.sp = re.compile(r'^(\s{1,2}|<bullet>)(?P<name>((((Mr)|(Ms)|(Mrs)|(Miss))\. (([-A-Z\'])(\s)?)+( of [A-Z][a-z]+)?)|((The ((VICE|ACTING|Acting) )?(PRESIDENT|SPEAKER|CHAIR(MAN)?)( pro tempore)?)|(The PRESIDING OFFICER)|(The CLERK)|(The CHIEF JUSTICE)|(The VICE PRESIDENT)|(Mr\. Counsel [A-Z]+))( \([A-Za-z.\- ]+\))?))\.')

    def test_fixedLineBreak(self):
        rootdir =  'tests/test_files/CREC-2005-07-20/json'
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
