import sys
import unittest
import os
import re

from fdsys import cr_parser 

class test_results(unittest.TestCase):

	# the parser is supposed to ignore front matter
	def test_ignore_files(self):
		cr_parser.parse_directory("test/test_files/front_matter", logdir="test/test_output/trash", outdir="test/test_output")
		# make sure test_files/front_matter/__parsed doesn't exist with a sample from the House and Senate
		self.assertTrue(not os.path.exists('test/test_output/__parsed'))

	# identifying speakers 
	def test_mr(self):
		content = cr_parser.parse_to_string("test/test_files/names/CREC-2013-01-23-pt1-PgE49-2.txt", logdir="test/test_output/trash", outdir="test/test_output")
		content = str(content)
		speaker = len(re.findall('<speaker name="Mr. POE of Texas">', content))
		speaking = len(re.findall('<speaking name="Mr. POE of Texas">', content))
		
		self.assertEqual(speaker, 1)
		self.assertEqual(speaking, 8)

	def test_ms(self):
		content = cr_parser.parse_to_string("test/test_files/names/CREC-2013-01-23-pt1-PgE50-3.txt", logdir="test/test_output/trash", outdir="test/test_output")
		content = str(content)
		speaker = len(re.findall('<speaker name="Ms. CASTOR of Florida">', content))
		speaking = len(re.findall('<speaking name="Ms. CASTOR of Florida">', content))
		
		self.assertEqual(speaker, 1)
		self.assertEqual(speaking, 5)

	def test_mrs(self):
		content = cr_parser.parse_to_string("test/test_files/names/CREC-2013-01-23-pt1-PgE53.txt", logdir="test/test_output/trash", outdir="test/test_output")
		content = str(content)
		speaker = len(re.findall('<speaker name="Mrs. BUSTOS">', content))
		speaking = len(re.findall('<speaking name="Mrs. BUSTOS">', content))

		self.assertEqual(speaker, 1)
		self.assertEqual(speaking, 4)
	
	def test_with_state(self):
		content = cr_parser.parse_to_string("test/test_files/names/CREC-2013-01-23-pt1-PgE53-4.txt", logdir="test/test_output/trash", outdir="test/test_output")
		content = str(content)
		speaker = len(re.findall('<speaker name="Ms. SEWELL of Alabama">', content))
		speaking = len(re.findall('<speaking name="Ms. SEWELL of Alabama">', content))
		
		self.assertEqual(speaker, 1)
		self.assertEqual(speaking, 7)
	
	def test_speaker(self):
		content = cr_parser.parse_to_string("test/test_files/names/CREC-2013-01-23-pt1-PgH225-5.txt", logdir="test/test_output/trash", outdir="test/test_output")
		content = str(content)
		speaker = len(re.findall('<speaker name="The SPEAKER">', content))
		speaking = len(re.findall('<speaking name="The SPEAKER">', content))
		
		self.assertEqual(speaker, 1)
		self.assertEqual(speaking, 1)

	def test_protempore(self):
		content = cr_parser.parse_to_string("test/test_files/names/CREC-2013-01-23-pt1-PgH251-2.txt", logdir="test/test_output/trash", outdir="test/test_output")
		content = str(content)
		speaker = len(re.findall('<speaker name="The SPEAKER pro tempore">', content))
		speaking = len(re.findall('<speaking name="The SPEAKER pro tempore">', content))

		self.assertEqual(speaker, 1)
		self.assertEqual(speaking, 3)

	def test_acting_protemp(slef):
		content = cr_parser.parse_to_string("test/test_files/names/CREC-2013-01-23-pt1-PgS189-5.txt", logdir="test/test_output/trash", outdir="test/test_output")
		content = str(content)
		speaker = len(re.findall('<speaker name="The ACTING PRESIDENT pro tempore">', content))
		speaking = len(re.findall('<speaking name="The ACTING PRESIDENT pro tempore">', content))

		self.assertEqual(speaker, 1)
		self.assertEqual(speaking, 1)

	def test_presiding(self):
		content = cr_parser.parse_to_string("test/test_files/names/CREC-2013-01-23-pt1-PgS226-5.txt", logdir="test/test_output/trash", outdir="test/test_output")
		content = str(content)
		speaker = len(re.findall('<speaker name="The PRESIDING OFFICER">', content))
		speaking = len(re.findall('<speaking name="The PRESIDING OFFICER">', content))
		
		self.assertEqual(speaker, 2)
		self.assertEqual(speaking, 3)

	def test_recorder(self):
		content = cr_parser.parse_to_string("test/test_files/names/CREC-2013-01-23-pt1-PgH225-7.txt", logdir="test/test_output/trash", outdir="test/test_output")
		content = str(content)
		speaker = len(re.findall("<recorder>", content))
		
		self.assertEqual(speaker, 1)
		

		# I still need to test Chair, Chairman, Clerk, The Cheif Justice and The Vice President. Also, I haven't found a Miss. but I don't think it is likely)

		
		
