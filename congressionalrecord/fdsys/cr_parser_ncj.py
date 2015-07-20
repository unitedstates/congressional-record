from bs4 import BeautifulSoup
from io import StringIO, BytesIO
import os
from datetime import datetime
	
class ParseCRDir(object):
	
	def gen_dir_metadata(self):
		''' Load up all metadata for this directory
		 from the mods file.'''
		with open(self.mods_path,'r') as mods_file:
			self.mods = BeautifulSoup(mods_file)
		
	def __init__(self, abspath, **kwargs):
		
		# dir data
        self.cr_dir = abspath
        self.mods_path = os.path.join(self.cr_dir,'mods.xml')
        self.html_path = os.path.join(self.cr_dir,'html')
    
class ParseCRFile(object):
	# Some regex
	re_time = r'^CREC-(?P<year>[0-9]{4})-(?P<month>[0-9]{2})-(?P<day>[0-9]{2})-.*'
	re_vol = r'Congressional Record Vol. (?P<vol>[0-9]+), No. (?P<num>[0-9]+)$'
	re_vol_file = r'^\n\[Congressional Record Volume (?P<vol>[0-9]+), Number (?P<num>[0-9]+)'
	                         + r'\((?P<wkday>[A-Za-z]+),(?P<month>[A-Za-z]+) (?P<day>[0-9]+),(?P<year>[0-9]{4})\)\]'
	                         + r'\n\[(?P<chamber>[A-Za-z]+)\]'
	                         + r'\n\[(?P<pages>\w+)\]'
	                         + r'\nFrom the Congressional Record Online'
	                         + r'through the Government Publishing Office \[www.gpo.gov\]$'
	re_recorderstart =      (r'^\s+(?P<start>'
                             + r'(The (assistant )?legislative clerk read as follows)'
                             + r'|(The nomination considered and confirmed is as follows)'
                             + r'|(The (assistant )?legislative clerk)'
                             + r'|(The nomination was confirmed)'
                             + r'|(There being no objection, )'
                             + r'|(The resolution .*?was agreed to.)'
                             + r'|(The preamble was agreed to.)'
                             + r'|(The resolution .*?reads as follows)'
                             + r'|(The assistant editor .*?proceeded to call the roll)'
                             + r'|(The bill clerk proceeded to call the roll.)'
                             + r'|(The bill clerk called the roll.)'
                             + r'|(The motion was agreed to.)'
                             #+ r'|(The Clerk read the resolution, as follows:)'
                             + r'|(The Clerk read (the resolution, )as follows:)'
                             + r'|(The resolution(, with its preamble,)? reads as follows:)'
                             + r'|(The amend(ment|ed).*?(is)? as follows:)'
                             + r'|(Amendment No\. \d+.*?is as follows:)'
                             + r'|(The yeas and nays resulted.*?, as follows:)'
                             + r'|(The yeas and nays were ordered)'
                             + r'|(The result was announced.*?, as follows:)'
                             + r'|(The .*?editor of the Daily Digest)'
                             + r'|(The (assistant )?bill clerk read as follows:)'
                             + r'|(The .*?read as follows:)'
                             + r'|(The text of the.*?is as follows)'
                             + r'|(amended( to read)? as follows:)'
                             + r'|(The material (previously )?referred to (by.*?)?is as follows:)'
                             + r'|(There was no objection)'
                             + r'|(The amendment.*?was agreed to)'
                             + r'|(The motion to table was .*)'
                             + r'|(The question was taken(;|.))'
                             + r'|(The following bills and joint resolutions were introduced.*)'
                             + r'|(The vote was taken by electronic device)'
                             + r'|(A recorded vote was ordered)'
                             #+ r'|()'
                            + r').*')
	re_allcaps = r'^\n  \s+(?P<title>[^a-z]+)'
             
                            
	# Some metadata
	self.doc_title = 'Parser did not find a title'
	self.speakers = []	
	self.doc_ref = ''
	self.doc_time = -1
	self.doc_start_time = -1
	self.doc_stop_time = -1
	self.doc_duration = -1
	self.doc_chamber = 'Unspecified'
	
	# Metadata-making functions
	def make_re_newspeaker(self):
		speaker_list = '|'.join([mbr for mbr in self.speakers.keys()])
		re_speakers = r'^(  |<bullet> )(?P<name>((' + speaker_list + ')|(((The ((VICE|ACTING|Acting) )?(PRESIDENT|SPEAKER|CHAIR(MAN)?)( pro tempore)?)|(The PRESIDING OFFICER)|(The CLERK)|(The CHIEF JUSTICE)|(The VICE PRESIDENT)|(Mr\. Counsel [A-Z]+))( \([A-Za-z.\- ]+\))?)\.))'
		return re_speakers
	
	def find_people(self):
		mbrs = self.doc_ref.find_all('congmember')
		if mbrs:
			for mbr in mbrs:
				nm = mbr.find('name',{'type':'parsed'}).string
				self.speakers[nm] = { \
				'bioguideid':mbr['bioguideid'], 'chamber':mbr['chamber'], \
				'congress':mbr['congress'], 'party':mbr['party'], \
				'role':mbr['role'], 'state':mbr['state'], \
				'name_full':mbr.find('name',{'type':'authority-fnf'}).string \
				}
	
	def date_from_entry(self):
		year, month, day = re.match(re_time,self.access_id)
		if self.doc_ref.time:
			from_hr,from_min,from_sec = self.doc_ref.time['from'].split(':')
			to_hr,to_min,to_sec = self.doc_ref.time['to'].split(':')
			self.doc_date = datetime.datetime(int(year),int(month),int(day))
			self.doc_start_time = datetime.datetime(int(year),int(month),int(day),\
			int(from_hr),int(from_min),int(from_sec))
			self.doc_stop_time = datetime.datetime(int(year),int(month),int(day),\
			int(to_hr),int(to_min),int(to_sec))
			self.doc_duration = self.doc_stop_time - self.doc_start_time
	
	# Flow control for metadata generation
	def gen_file_metadata(self):
		self.doc_ref = cr_dir.mods.find('accessid', text=self.access_id).parent
		self.doc_title, cr_loc = self.doc_ref.searchtitle.string.split(';')
		self.find_people()
		self.date_from_entry()
		self.chamber = self.doc_ref.granuleclass.string
		self.cr_vol, self.cr_num = re.match(re_vol,cr_loc)
		self.re_newspeaker = make_re_newspeaker()

	def read_htm_file(self):
		with open(self.filepath, 'r') as htm_file:
			htm_lines = htm_file.read()
			htm_text = BeautifulSoup(htm_lines)
		text = htm_text.pre.text.split('\n\n')
		for line in text:
			self.line_no += 1
			yield text
			
	def write_header(self,outfile):
		outfile.write('<CRDoc>\n')
		header_in = self.the_text.next()
        vol, num, wkday, month, day, year, chamber, pages = re.match(self.re_vol_file, header_in)
        header_out = '<header vol={0} num={1} wkday={2} month={3} day={4} year={5} chamber={6} pages={7}></header>'.format(\
        vol, num, wkday, month, day, year, chamber, pages)
        outfile.write(header_out + '\n')
        
    def write_body(self,outfile):
		for line in self.the_text:
			if line == u'':
				next_line = self.the_text.next()
		
		
				

			

	def make_xml_file(self, outdir, the_text=self.the_text):
		self.outpath = os.path.join(outdir, self.access_id + '.xml')
		with open(outpath,'w') as outfile:
			self.line_no = 0
			self.write_header(outfile)
			self.write_body(outfile)
			self.write_footer(outfile)
	
	def parse(self):
		self.the_text = self.read_htm_file()
		
	def __init__(self, abspath, cr_dir, **kwargs):
		# file data
		self.filepath = abspath
        self.filedir, self.filename = os.path.split(self.filepath)
        self.outdir = kwargs['outdir']
        self.access_id = self.filename.split('.')[0]
		
		# Generate all metadata including list of speakers
        self.gen_file_metadata()
        
        # Parse the file
        self.line_no = 0
        self.parse()
        
        
        
		
        
