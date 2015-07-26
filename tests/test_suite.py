import unittest
from congressionalrecord.fdsys import cr_parser as cr
import random
import os

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
