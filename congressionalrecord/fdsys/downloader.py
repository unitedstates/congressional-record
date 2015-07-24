import requests
import os
from datetime import datetime,date,timedelta
from time import sleep
from zipfile import ZipFile
from cr_parser import ParseCRDir, ParseCRFile
import json
from pyselasticsearch import ElasticSearch

class elasticSearchStack(object)
    """
    Accepts crdoc objects (python dicts) and stores them as a list until
    <chunk_size> are present. Then, passes those objects to es bulk index API
    and updates the stack.
    """
    def stackwatch(self,**kwargs):
        while self.run == True:
            if len(self.stack) > kwargs['chunk_size']:
                output = self.stack[0:kwargs['chunk_size']]
                es.bulk((es.index_op(doc,id=doc.pop('id')) for doc in output),
                        index = kwargs['index'])
                self.stack = self.stack[kwargs['chunk_size']:]
                 

    def __init__(self, chunk_size = 100,es_url = 'http://localhost:9200', **kwargs):
        self.es_conn = ElasticSearch(es_url)
        self.stack = []
        self.run = True
        
        
class Downloader(object):
    """
    Bulk downloads will pass objects to the tail end of a stack in a stack object.
    The stack object should bulk index things <chunk> at a time.
    """
    def bulkdownload(self,start,parse=True,**kwargs):
        day = datetime.strptime(start,'%Y-%m-%d')
        if 'end' in kwargs.keys():
            end = kwargs['end']
        else:
            end = start
        end_day = datetime.strptime(end,'%Y-%m-%d')
        while day <= end_day:
            day_str = datetime.strftime(day,'%Y-%m-%d')
            fdsysExtract(day_str,**kwargs)
            if parse:
                dir_str = 'CREC-' + day_str
                year_str = str(day.year)
                if 'outpath' not in kwargs.keys():
                    outpath = 'output'
                else:
                    outpath = kwargs['outpath']
                try:
                    dir_path = os.path.join(outpath,year_str,dir_str)
                    crdir = ParseCRDir(dir_path)
                    for the_file in os.listdir(os.path.join(dir_path,'html')):
                        parse_path = os.path.join(dir_path,'html',the_file)
                        if '-PgD' in parse_path or 'FrontMatter' in parse_path:
                            print 'Skipping {0}'.format(parse_path)
                        else:
                            crfile = ParseCRFile(parse_path,crdir)
                            handle_crfile(crfile,**kwargs)
                except IOError, e:
                    print '{0}, skipping.'.format(e)
            day += timedelta(days=1)

    def handle_crfile(self,crfile,**kwargs):
        """
         do_mode is either 'json' (write JSON to flatfiles)
         or 'es' (index on elasticsearch)
        """
        if 'do_mode' in kwargs.keys():
            do_mode = kwargs['do_mode']
        else:
            do_mode = 'pass'
        if do_mode == 'json':
            filename = os.path.split(crfile.filepath)[-1].split('.')[0] + '.json'
            outpath = os.path.split(crfile.filepath)[0]
            outpath = os.path.split(outpath)[0]
            if 'json' not in os.listdir(outpath):
                os.mkdir(os.path.join(outpath,'json'))
            outpath = os.path.join(outpath,'json',filename)
            with open(outpath,'w') as out_json:
                json.dump(crfile.crdoc,out_json)
        elif do_mode == 'es':
            assert 'es_stack' in kwargs.keys(), 'Must specify ElasticSearch stack'
            kwargs['es_stack'].stack.append(crfile.crdoc)
        else:
            print 'Unknown mode {0}'.format(do_mode)
            pass

    def __init__(self,start,parse,**kwargs):
        # ex. es_stack = ElasticSearch stack object
        # outpath = output (specified by default)
        # do_mode = es (default 'pass')
        # end = ending date
        self.bulkdownload(start,parse,**kwargs)
            
        

class downloadRequest(object):

    its_today = date.strftime(date.today(),'%Y-%m-%d')
    
    def knock(self,url):
        try:
            r = requests.get(url)
            if r.status_code == requests.codes.ok:
                binary_content = r.content
            else:
                binary_content = False
                r.raise_for_status()
                print 'Download returned status code %s' % str(r.status_code)
                
        except (requests.exceptions.ConnectionError,requests.exceptions.HTTPError) as ce:
            print 'Connection error: %s' % ce
            binary_content = False
            if r.status_code == 404:
                self.status = 404
        return binary_content

    def __init__(self,url,filename,n_tries=3):
        self.status = False
        print 'Download request: %s, made on %s' % (url,self.its_today)
        while n_tries > 0:
            print 'Attempting download ...'
            binary_content = self.knock(url)
            self.binary_content = binary_content
            if self.binary_content:
                print 'Request returned results.'
                n_tries = 0
            elif self.status == 404:
                print 'File not found, skipping.'
                break
            else:
                n_tries -= 1
                sleep(15)
        if self.binary_content:
            with open(filename,'wb') as outfile:
                outfile.write(self.binary_content)
            print 'Wrote {0}'.format(filename)
            self.status = True
        else:            
            print 'No download for {0}'.format(url)
            

    
class fdsysDL(object):
    fdsys_base = 'http://www.gpo.gov/fdsys/pkg/CREC-'
    
    def download_day(self,day,outpath):
        assert datetime.strptime(day,"%Y-%m-%d"), "Malformed date field. Must be 'YYYY-MM-DD'"
        the_url = self.fdsys_base + day + '.zip'
        dl_time = datetime.strptime(day,"%Y-%m-%d")
        year = str(dl_time.year)
        if year not in os.listdir(outpath):
            os.mkdir(os.path.join(outpath,year))
        the_filename = os.path.join(outpath,year,'CREC-' + day + '.zip')
        the_download = downloadRequest(the_url,the_filename)
        self.status = the_download.status
        if the_download.status == False:
            print "Download for {0} did not complete.".format(day)
        elif the_download.status == 404:
            print 'Download for {0} did not complete because there is no record for that day.'.format(day)

    def __init__(self,day,**kwargs):
        if 'outpath' in kwargs.keys():
            self.outpath = kwargs['outpath']
        else:
            if 'output' not in os.listdir(os.getcwd()):
                os.mkdir('output')
            self.outpath = 'output'
        self.download_day(day,self.outpath)

class fdsysExtract(object):

    def __init__(self,day,**kwargs):
        assert datetime.strptime(day,"%Y-%m-%d"), "Malformed date field. Must be 'YYYY-MM-DD'"
        dl_time = datetime.strptime(day,"%Y-%m-%d")
        year = str(dl_time.year)
        if 'outpath' not in kwargs.keys():
            outpath = 'output'
        else:
            outpath = kwargs['outpath']
        abspath = os.path.join(outpath,year,'CREC-' + day + '.zip')
        extract_to = 'CREC-' + day
        if extract_to in os.listdir(os.path.join(outpath,year)):
            print "{0} already exists in extraction tree.".format(extract_to)
            return None
        if extract_to + '.zip' not in os.listdir(os.path.join(outpath,year)):
            the_dl = fdsysDL(day,outpath=outpath)
            if the_dl.status == 404:
                print 'No record on this day, not trying to extract'
                return None
        with ZipFile(abspath,'r') as the_zip:
            the_zip.extractall(os.path.join(outpath,year))
            print 'Extracted to {0}'.format(os.path.join(outpath,year))
        os.remove(abspath)



        

        
