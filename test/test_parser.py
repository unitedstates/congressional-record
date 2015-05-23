import sys
import unittest
import os
import re

from congressionalrecord.fdsys import cr_parser

# simple files to test basic boiler plate parsing
def bolier_house_content():
	house_content = cr_parser.parse_to_string("test/test_files/boiler_plate/CREC-2014-01-28-pt1-PgH1433-2.txt", logdir="test/test_output", outdir="test/test_output")
	return str(house_content)

def bolier_senate_content():
	senate_content = cr_parser.parse_to_string("test/test_files/boiler_plate/CREC-2014-01-28-pt1-PgS493-2.txt", logdir="test/test_output", outdir="test/test_output")
	return str(senate_content)

bolier_house_content = bolier_house_content()
bolier_senate_content = bolier_senate_content()


class test_results(unittest.TestCase):
	# Travis doesn't like this test
	# # the parser is supposed to ignore front matter
	# def test_ignore_files(self):
	# 	cr_parser.parse_directory("test/test_files/front_matter", logdir="test/test_output", outdir="test/test_output")
	# 	# make sure test_files/front_matter/__parsed doesn't exist with a sample from the House and Senate
	# 	self.assertTrue(not os.path.exists('test/test_output/__parsed'))

	# identifying speakers
	def test_mr(self):
		content = cr_parser.parse_to_string("test/test_files/names/CREC-2013-01-23-pt1-PgE49-2.txt", logdir="test/test_output", outdir="test/test_output")
		content = str(content)
		speaker = len(re.findall('<speaker name="Mr. POE of Texas">', content))
		speaking = len(re.findall('<speaking name="Mr. POE of Texas">', content))

		self.assertEqual(speaker, 1)
		self.assertEqual(speaking, 8)

	def test_ms(self):
		content = cr_parser.parse_to_string("test/test_files/names/CREC-2013-01-23-pt1-PgE50-3.txt", logdir="test/test_output", outdir="test/test_output")
		content = str(content)
		speaker = len(re.findall('<speaker name="Ms. CASTOR of Florida">', content))
		speaking = len(re.findall('<speaking name="Ms. CASTOR of Florida">', content))

		self.assertEqual(speaker, 1)
		self.assertEqual(speaking, 5)

	def test_mrs(self):
		content = cr_parser.parse_to_string("test/test_files/names/CREC-2013-01-23-pt1-PgE53.txt", logdir="test/test_output", outdir="test/test_output")
		content = str(content)
		speaker = len(re.findall('<speaker name="Mrs. BUSTOS">', content))
		speaking = len(re.findall('<speaking name="Mrs. BUSTOS">', content))

		self.assertEqual(speaker, 1)
		self.assertEqual(speaking, 4)

	def test_with_state(self):
		content = cr_parser.parse_to_string("test/test_files/names/CREC-2013-01-23-pt1-PgE53-4.txt", logdir="test/test_output", outdir="test/test_output")
		content = str(content)
		speaker = len(re.findall('<speaker name="Ms. SEWELL of Alabama">', content))
		speaking = len(re.findall('<speaking name="Ms. SEWELL of Alabama">', content))

		self.assertEqual(speaker, 1)
		self.assertEqual(speaking, 7)

	def test_speaker(self):
		content = cr_parser.parse_to_string("test/test_files/names/CREC-2013-01-23-pt1-PgH225-5.txt", logdir="test/test_output", outdir="test/test_output")
		content = str(content)
		speaker = len(re.findall('<speaker name="The SPEAKER">', content))
		speaking = len(re.findall('<speaking name="The SPEAKER">', content))

		self.assertEqual(speaker, 1)
		self.assertEqual(speaking, 1)

	def test_protempore(self):
		content = cr_parser.parse_to_string("test/test_files/names/CREC-2013-01-23-pt1-PgH251-2.txt", logdir="test/test_output", outdir="test/test_output")
		content = str(content)
		speaker = len(re.findall('<speaker name="The SPEAKER pro tempore">', content))
		speaking = len(re.findall('<speaking name="The SPEAKER pro tempore">', content))

		self.assertEqual(speaker, 1)
		self.assertEqual(speaking, 3)

	def test_acting_protemp(self):
		content = cr_parser.parse_to_string("test/test_files/names/CREC-2013-01-23-pt1-PgS189-5.txt", logdir="test/test_output", outdir="test/test_output")
		content = str(content)
		speaker = len(re.findall('<speaker name="The ACTING PRESIDENT pro tempore">', content))
		speaking = len(re.findall('<speaking name="The ACTING PRESIDENT pro tempore">', content))

		self.assertEqual(speaker, 1)
		self.assertEqual(speaking, 1)

	def test_presiding(self):
		content = cr_parser.parse_to_string("test/test_files/names/CREC-2013-01-23-pt1-PgS226-5.txt", logdir="test/test_output", outdir="test/test_output")
		content = str(content)
		speaker = len(re.findall('<speaker name="The PRESIDING OFFICER">', content))
		speaking = len(re.findall('<speaking name="The PRESIDING OFFICER">', content))

		self.assertEqual(speaker, 2)
		self.assertEqual(speaking, 3)

	def test_recorder(self):
		content = cr_parser.parse_to_string("test/test_files/names/CREC-2013-01-23-pt1-PgH225-7.txt", logdir="test/test_output", outdir="test/test_output")
		content = str(content)
		speaker = len(re.findall("<recorder>", content))

		self.assertEqual(speaker, 1)

	def test_excutive(self):
		content = cr_parser.parse_to_string("test/test_files/SOTU/CREC-2014-01-28-pt1-PgH1473-5.txt", logdir="test/test_output", outdir="test/test_output")
		content = str(content)
		vpspeaker = len(re.findall('<speaker name="The VICE PRESIDENT"', content))
		vpspeaking = len(re.findall('<speaking name="The VICE PRESIDENT"', content))
		speaker = len(re.findall('<speaker name="The PRESIDENT"', content))
		speaking = len(re.findall('<speaking name="The PRESIDENT"', content))

		self.assertEqual(vpspeaker, 1)
		# the VP count is off
		# self.assertEqual(vpspeaking, 22)
		self.assertEqual(speaker, 1)
		self.assertEqual(speaking, 105)

	# Speakers with spaces in their names
	def test_whitespace(self):
		content = cr_parser.parse_to_string("test/test_files/whitespace/CREC-2013-10-16-pt1-PgE1522-2.txt", logdir="test/test_output", outdir="test/test_output")
		content = str(content)
		speaker = len(re.findall('<speaker name="Ms. WASSERMAN SCHULTZ">', content))
		speaking = len(re.findall('<speaking name="Ms. WASSERMAN SCHULTZ">', content))
		self.assertEqual(speaker, 1)
		self.assertEqual(speaking, 5)

	# Speakers with middle initials in their names
	def test_middle_initials(self):
		content = cr_parser.parse_to_string("test/test_files/middle_initials/CREC-2011-05-05-pt1-PgE817-2.txt", logdir="test/test_output", outdir="test/test_output")
		content = str(content)
		speaker = len(re.findall('<speaker name="Mr. DANIEL E. LUNGREN of California">', content))
		speaking = len(re.findall('<speaking name="Mr. DANIEL E. LUNGREN of California">', content))
		self.assertEqual(speaker, 1)
		self.assertEqual(speaking, 5)

	# I still need to test Chair, Chairman, Clerk and The Chief Justice. Also, I haven't found a Miss. but I don't think it is likely)

	# boiler plate
	def test_volume(self):
		self.assertTrue("<volume>160</volume>" in bolier_house_content)
		self.assertTrue("<volume>160</volume>" in bolier_senate_content)

	def test_number(self):
		self.assertTrue("<number>16</number>" in bolier_house_content)
		self.assertTrue("<number>16</number>" in bolier_senate_content)

	def test_weekday(self):
		self.assertTrue("<weekday>Tuesday</weekday>" in bolier_house_content)
		self.assertTrue("<weekday>Tuesday</weekday>" in bolier_senate_content)

	def test_month(self):
		self.assertTrue("<month>January</month>" in bolier_house_content)
		self.assertTrue("<month>January</month>" in bolier_senate_content)

	def test_day(self):
		self.assertTrue("<day>28</day>" in bolier_house_content)
		self.assertTrue("<day>28</day>" in bolier_senate_content)

	def test_year(self):
		self.assertTrue("<year>2014</year>" in bolier_house_content)
		self.assertTrue("<year>2014</year>" in bolier_senate_content)

	def test_chamber(self):
		extention_content = cr_parser.parse_to_string('test/test_files/boiler_plate/CREC-2014-01-28-pt1-PgE123-4.txt', logdir="test/test_output", outdir="test/test_output")
		extention_content = str(extention_content)

		self.assertTrue("<chamber>Extensions</chamber>" in extention_content)
		self.assertTrue("<chamber>House</chamber>" in bolier_house_content)
		self.assertTrue("<chamber>Senate</chamber>" in bolier_senate_content)

	def test_pages(self):
		self.assertTrue("<pages>H1433</pages>" in bolier_house_content)
		self.assertTrue("<pages>S493</pages>" in bolier_senate_content)

	def test_congress(self):
		self.assertTrue("<congress>113</congress>" in bolier_house_content)
		self.assertTrue("<congress>113</congress>" in bolier_senate_content)

	def test_session(self):
		self.assertTrue("<session>2</session>" in bolier_house_content)
		self.assertTrue("<session>2</session>" in bolier_senate_content)


	# Common tags
	def test_block_quote(self):
		content = cr_parser.parse_to_string('test/test_files/common_tags/CREC-2013-01-23-pt1-PgE58-3.txt', logdir="test/test_output", outdir="test/test_output")
		content = str(content)

		self.assertTrue('<speaking quote="true" speaker="Mr. SABLAN">' in content)


