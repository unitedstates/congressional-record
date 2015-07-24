import requests
import os
from datetime import datetime,date,timedelta
from time import sleep
from zipfile import ZipFile

def bulkdownload(start,end,**kwargs):
    day = datetime.strptime(start,'%Y-%m-%d')
    end_day = datetime.strptime(end,'%Y-%m-%d')
    while day <= end_day:
        day_str = datetime.strftime(day,'%Y-%m-%d')
        fdsysExtract(day_str)
        day += timedelta(days=1)        
        
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



        

        
