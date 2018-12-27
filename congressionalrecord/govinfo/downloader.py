from __future__ import absolute_import
#import requests
from builtins import str
from builtins import object
import certifi
import urllib3.contrib.pyopenssl
urllib3.contrib.pyopenssl.inject_into_urllib3()
from urllib3 import PoolManager, Retry, Timeout
import os
from datetime import datetime, date, timedelta
from time import sleep
from zipfile import ZipFile
from .cr_parser import ParseCRDir, ParseCRFile
import json
from pyelasticsearch import ElasticSearch, bulk_chunks
import logging


class Downloader(object):
    """
    Chunks through downloads and is ready to pass
    to elasticsearch or yield json.
    """
    def bulkdownload(self, start, parse=True, **kwargs):
        day = datetime.strptime(start, '%Y-%m-%d')
        if 'end' in list(kwargs.keys()):
            end = kwargs['end']
        else:
            end = start
        end_day = datetime.strptime(end, '%Y-%m-%d')
        while day <= end_day:
            day_str = datetime.strftime(day, '%Y-%m-%d')
            extractor = GovInfoExtract(day_str, **kwargs)
            self.status = extractor.status
            if self.status == 404:
                logging.info('bulkdownloader skipping a missing day.')
            elif parse:
                dir_str = 'CREC-' + day_str
                year_str = str(day.year)
                if 'outpath' not in list(kwargs.keys()):
                    outpath = 'output'
                else:
                    outpath = kwargs['outpath']
                try:
                    dir_path = os.path.join(outpath, year_str, dir_str)
                    crdir = ParseCRDir(dir_path)
                    for the_file in os.listdir(os.path.join(dir_path, 'html')):
                        parse_path = os.path.join(dir_path, 'html', the_file)
                        if any(('-PgD' in parse_path,
                                'FrontMatter' in parse_path,
                                '-Pgnull' in parse_path)):
                            logging.info('Skipping {}'.format(parse_path))
                        else:
                            crfile = ParseCRFile(parse_path, crdir)
                            yield crfile
                except IOError as e:
                    logging.warning('{}, skipping.'.format(e))
            else:
                logging.warning('Unexpected condition in bulkdownloader')
            day += timedelta(days=1)


    def __init__(self, start, **kwargs):
        """
        Invoke a Downloader object to get data from
        the Record. It will check to see if the necessary
        files are already downloaded and use those instead of
        querying FDSys. Downloaders are the endpoint for raw data.

        Required arguments:

        start : In form 'YYYY-MM-DD.' This is the day/start day you want.

        Optional arguments:

        parse : Defaults to True. This tells the downloader whether you just want
                the raw files, or if you also want it to extract data from the HTML.
                (Default means yes, give me the data.)


        end : Same form as start. This is the end date.

        outpath : Output path RELATIVE TO the present working directory. Defaults
                  to 'output' and works fine when you run it from the repo's root
                  directory.

        do_mode : Specify what kind of data you want from the parser.
                  If do_mode is not set, the downloader will do absolutely zilch.
                  do_mode can take the following values:

                  json : write json files in a /json directory for that
                         day of the Record.

                  es : Specify the URL and index of an ElasticSearch cluster with
                       arguments es_url and index, and it will pass each file to
                       that cluster for indexing. WARNING: This doesn't handle any
                       mappings, and it doesn't check to see if records are already
                       there, so it will overwrite old files in the same index
                       WITHOUT versioning.

                       also specify:
                       es_url : ElasticSearch cluster url
                       index  : ElasticSearch cluster index

                  yield : For each day of the Record the user specifies,
                          the downloader acts like a generator, yielding that day's
                          "crfile" dictionary.
        """
        self.status = 'idle'
        logging.debug('Downloader object ready with params:')
        logging.debug(', '.join(['='.join([key, value]) for key, value in list(kwargs.items())]))
        if 'outpath' in list(kwargs.keys()):
            outpath = kwargs['outpath']
        else:
            outpath = 'output'
        if kwargs['do_mode'] == 'es':
            es = ElasticSearch(kwargs['es_url'])
            for chunk in bulk_chunks((es.index_op(crfile.crdoc, id=crfile.crdoc.pop('id')) for crfile
                                        in self.bulkdownload(start, **kwargs)),
                                        docs_per_chunk=100):
                es.bulk(chunk, index=kwargs['index'], doc_type='crdoc')
        elif kwargs['do_mode'] == 'json':
            # outpath called so often to make it easy to follow
            # the idea that we're traversing a directory tree
            for crfile in self.bulkdownload(start, **kwargs):
                filename = os.path.split(crfile.filepath)[-1].split('.')[0] + '.json'
                outpath = os.path.split(crfile.filepath)[0]
                outpath = os.path.split(outpath)[0]
                if 'json' not in os.listdir(outpath):
                    os.mkdir(os.path.join(outpath, 'json'))
                outpath = os.path.join(outpath, 'json', filename)
                with open(outpath, 'w') as out_json:
                    json.dump(crfile.crdoc, out_json)
        elif kwargs['do_mode'] == 'yield':
            self.yielded = self.bulkdownload(start, parse=True, **kwargs)
        elif kwargs['do_mode'] == 'noparse':
            self.bulkdownload(start, parse=False, **kwargs)

        else:
            return None





class downloadRequest(object):

    user_agent = {'user-agent': 'congressional-record 0.0.1 (https://github.com/unitedstates/congressional-record)'}
    its_today = datetime.strftime(datetime.today(), '%Y-%m-%d %H:%M')
    timeout = Timeout(connect=2.0, read=10.0)
    retry = Retry(total=3, backoff_factor=300)
    retry.BACKOFF_MAX = 602
    http = PoolManager(timeout=timeout, retries=retry,
                       cert_reqs='CERT_REQUIRED',
                       ca_certs=certifi.where(),
                       headers=user_agent)

    def __init__(self, url, filename):
        self.status = False
        try:
            logging.info('Sending request on {}'.format(self.its_today))
            r = self.http.request('GET', url)
            logging.debug('Request headers received with code {}'.format(r.status))
            if r.status == 404:
                logging.warn('Received 404, not retrying request.')
                self.status = 404
            elif r.status == 200 and r.data:
                logging.info('Considering request successful.')
                self.binary_content = r.data
                self.status = True
            else:
                logging.warn('Unexpected condition, not continuing:\
                {}'.format(r.status))
        except urllib3.exceptions.MaxRetryError as ce:
            logging.warn('Error: %s - Aborting download' % ce)
        if self.status == False:
            logging.warn('Failed to download file {}'.format(url))
        elif self.status == 404:
            logging.info('downloadRequester skipping file that returned 404.')
        elif self.binary_content:
            with open(filename, 'wb') as outfile:
                outfile.write(self.binary_content)
            logging.info('Wrote {}'.format(filename))
        else:
            logging.info('No download for {} and terminating with unexpected condition.\n'.format(url))


class GovInfoDL(object):
    govinfo_cr_download_base = 'https://www.govinfo.gov/content/pkg/CREC-'

    def download_day(self, day, outpath):
        assert datetime.strptime(day, "%Y-%m-%d"), "Malformed date field. Must be 'YYYY-MM-DD'"
        the_url = self.govinfo_cr_download_base + day + '.zip'
        dl_time = datetime.strptime(day, "%Y-%m-%d")
        year = str(dl_time.year)
        if year not in os.listdir(outpath):
            os.mkdir(os.path.join(outpath, year))
        the_filename = os.path.join(outpath, year, 'CREC-' + day + '.zip')
        the_download = downloadRequest(the_url, the_filename)
        self.status = the_download.status
        if self.status == False:
            logging.warn("fdsysDL received report that download for {} did not complete.".format(day))
        elif self.status == 404:
            logging.warning('fdsysDL received 404 report for {}.'.format(day))
        else:
            logging.info('fdsysDL received expected condition {} for downloader'.format(the_download.status))

    def __init__(self, day, **kwargs):
        self.status = 'idle'
        if 'outpath' in list(kwargs.keys()):
            self.outpath = kwargs['outpath']
        else:
            self.outpath = 'output'
        self.download_day(day, self.outpath)

class GovInfoExtract(object):

    def __init__(self, day, **kwargs):
        self.status = 'idle'
        assert datetime.strptime(day, "%Y-%m-%d"), "Malformed date field. Must be 'YYYY-MM-DD'"
        dl_time = datetime.strptime(day, "%Y-%m-%d")
        year = str(dl_time.year)
        if 'outpath' not in list(kwargs.keys()):
            outpath = 'output'
        else:
            outpath = kwargs['outpath']
        if not os.path.isdir(outpath):
            os.makedirs(outpath)
        abspath = os.path.join(outpath, year, 'CREC-' + day + '.zip')
        extract_to = 'CREC-' + day
        if year not in os.listdir(outpath):
            os.mkdir(os.path.join(outpath, year))
        if extract_to in os.listdir(os.path.join(outpath, year)):
            logging.info("{} already exists in extraction tree.".format(
                extract_to))
            self.status = 'existingFiles'
            return None
        if extract_to + '.zip' not in os.listdir(os.path.join(outpath, year)):
            the_dl = GovInfoDL(day, outpath=outpath)
            self.status = the_dl.status
            if self.status is not True:
                logging.info('No record on this day, not trying to extract')
                self.status = 'downloadFailure'
                return None
        with ZipFile(abspath, 'r') as the_zip: # errors here
            the_zip.extractall(os.path.join(outpath, year))
            logging.info('Extracted to {}'.format(os.path.join(outpath,
                                                                year)))
            self.status = 'extractedFiles'
        os.remove(abspath)
        self.status += 'deletedZip'
        logging.info('Extractor completed with status {}'.format(self.status))
