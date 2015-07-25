import requests
import os
from datetime import datetime,date,timedelta
from time import sleep
from zipfile import ZipFile
from cr_parser import ParseCRDir, ParseCRFile
import json
from pyelasticsearch import ElasticSearch, bulk_chunks


class Downloader(object):
    """
    Bulk downloads will pass objects to the tail end of a stack in a stack object.
    The stack object should bulk index things <chunk> at a time.
    """
    def bulkdownload(self,start,**kwargs):
        day = datetime.strptime(start,'%Y-%m-%d')
        if 'end' in kwargs.keys():
            end = kwargs['end']
        else:
            end = start
        if 'parse' in kwargs.keys():
            parse = kwargs['parse']
        else:
            parse = True
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
                            yield crfile
                except IOError, e:
                    print '{0}, skipping.'.format(e)
            day += timedelta(days=1)

    def __init__(self,start,**kwargs):
        # ex. es_url = ElasticSearch service url
        # index = ElasticSearch index
        # outpath = output (specified by default)
        # do_mode = es (default 'pass')
        # end = ending date
        print 'Downloader object ready with params:'
        print ','.join(['='.join([key,value]) for key,value in kwargs.items()])
        if kwargs['do_mode'] == 'es':
            es = ElasticSearch(kwargs['es_url'])
            for chunk in bulk_chunks((es.index_op(crfile.crdoc,id=crfile.crdoc.pop('id')) for crfile
                                        in self.bulkdownload(start,**kwargs)),
                                        docs_per_chunk=100):
                es.bulk(chunk,index=kwargs['index'],doc_type='crdoc')
        elif kwargs['do_mode'] == 'json':
            # outpath called so often to make it easy to follow
            # the idea that we're traversing a directory tree
            for crfile in self.bulkdownload(start,**kwargs):
                filename = os.path.split(crfile.filepath)[-1].split('.')[0] + '.json'
                outpath = os.path.split(crfile.filepath)[0]
                outpath = os.path.split(outpath)[0]
                if 'json' not in os.listdir(outpath):
                    os.mkdir(os.path.join(outpath,'json'))
                outpath = os.path.join(outpath,'json',filename)
                with open(outpath,'w') as out_json:
                    json.dump(crfile.crdoc,out_json)
        else:
            return None
                                                                       
                            
        

class downloadRequest(object):

    its_today = date.strftime(date.today(),'%Y-%m-%d')
    
    def knock(self,url):
        try:
            r = requests.get(url)
            if r.status_code == requests.codes.ok:
                binary_content = r.content
            else:
                binary_content = False
                self.status = r.status_code
                print 'Download returned status code %s' % str(r.status_code)
                
        except (requests.exceptions.ConnectionError) as ce:
            print 'Connection error: %s' % ce
            binary_content = False
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
        if year not in os.listdir(outpath):
            os.mkdir(os.path.join(outpath,year))
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



        

        
