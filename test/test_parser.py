import sys
import unittest
import os

from fdsys import cr_parser 

class test_results(unittest.TestCase):

	# the parser is supposed to ignore front matter
	def test_ignore_files(self):
		cr_parser.parse_directory("test/test_files/front_matter",logdir="test/test_output/trash", outdir="test/test_output")
		# make sure test_files/front_matter/__parsed doesn't exist with a sample from the House and Senate
		self.assertTrue(not os.path.exists('test/test_output/__parsed'))

