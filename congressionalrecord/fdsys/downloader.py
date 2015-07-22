import requests
import os
from datetime import datetime

class downloadRequest(object):

    its_today = date.strftime(date.today(),'%Y-%m-%d')
    
    def knock(self,url):
        try:
            r = requests.get(url)
            if r.status_code == requests.codes.ok:
                binary_content = r.content
            else:
                binary_content = False
                print 'Download returned status code %s' % str(r.status_code)
        except requests.exceptions.ConnectionError, ce:
            print 'Connection error: %s' % ce
            binary_content = False
        return binary_content

    def __init__(self,url,filename,n_tries=3):
        print 'Download request: %s, made on %s' % (url,self.its_today)
        while n_tries > 0:
            print 'Attempting download ...'
            binary_content = self.knock(url)
            self.binary_content = binary_content
            if self.binary_content:
                print 'Request returned results.'
                n_tries = 0
            else:
                n_tries -= 1
                sleep(15)
        if self.binary_content:
            with open(filename,'wb') as outfile:
                outfile.write(r.content)
            print 'Wrote {0}'.format(filename)
            self.status = True
        else:            
            print 'No download for {0}'.format(url)
            self.status = False

    
class fdsysDL(object):
    fdsys_base = 'http://gpo.gov/fdsys/pkg/'
    
    def download_day(day,outpath):
        assert datetime.strptime(day,"%Y-%m-%d"), "Malformed date field. Must be 'YYYY-MM-DD'"
        the_url = fdsys_base + day + '.zip'
        dl_time = datetime.strptime(day,"%Y-%m-%d")
        if str(dl_time.year) not in os.listdir(outpath):
            os.mkdir(os.path.join(outpath,str(dl_time.year)))
        the_filename = os.path.join(outpath,year,day,'.zip')
        the_download = downloadRequest(the_url,the_filename)
        if the_download.status == False:
            raise Exception, "Download for {0} did not complete.".format(day)

    def __init__(day,**kwargs):
        if 'outpath' in kwargs.keys():
            self.outpath = kwargs['outpath']
        else:
            if 'output' not in os.listdir(os.getcwd()):
                os.mkdir('output')
            self.outpath = 'output'
        self.download_day(day,self.outpath)
        
        
