from builtins import str
from builtins import object
import psycopg2 as pc
from psycopg2.extras import RealDictCursor as rdc
from ..govinfo.downloader import Downloader as dl
from collections import OrderedDict
import logging
import unicodecsv as csv
import os

def if_exists(key,store):
    if key in list(store.keys()):
        return store[key]
    else:
        logging.warning('{0} not in {1}, returning default value'.format(key,store))
        return None

def rd(astring,delimiter='|'):
    outstr = astring.replace(delimiter,'')
    return outstr

class outStack(object):
    def add(self,a_page):
        self.stack.append(a_page)

    def write(self):
        while self.stack:
            row = self.stack.pop(0)
            self.writer.writerow(row)

    def __init__(self,outpath,fieldnames):
        """
        Stack object for managing rows.
        Args:
            outpath : File path string
            fieldnames : list of field names in order
        """
        self.outfile = open(outpath,'ab')
        self.stack = []
        self.writer = csv.DictWriter(self.outfile,fieldnames=fieldnames,
                                     delimiter='|',encoding='utf-8')

    

class crToPG(object):

    def ingest(self,crfile,pagestack,billstack,speechstack):
        """
        Break a crdoc into three parts
        Pass the appropriate rows for each part
        to the right stack for a bulk insert.
        """
        page_row =  OrderedDict([('pageid',crfile['id']),
                     ('title',rd(crfile['doc_title'])),
                     ('chamber',crfile['header']['chamber']),
                     ('extension',crfile['header']['extension']),
                     ('cr_day',crfile['header']['day']),
                     ('cr_month',crfile['header']['month']),
                     ('cr_year',crfile['header']['year']),
                     ('num',crfile['header']['num']),
                     ('vol',crfile['header']['vol']),
                     ('pages',crfile['header']['pages']),
                     ('wkday',crfile['header']['wkday'])
                   ])
        # Add the "page" level to the page stack first
        pagestack.add(page_row)

        bills = []
        if 'related_bills' in list(crfile.keys()):
            for bill in crfile['related_bills']:
                bill_row = OrderedDict([('congress',bill['congress']),
                            ('context',bill['context']),
                            ('bill_type',bill['type']),
                            ('bill_no',bill['number']),
                            ('pageid',crfile['id'])
                            ])
                bills.append(bill_row)

        # Bills for the bill god!
        billstack.add(bills)

        speeches = []
        for speech in crfile['content']:
            if speech['kind'] == 'speech':
                speechid = crfile['id'] + '-' + str(speech['turn'])
                speech_row = OrderedDict([('speechid',speechid),
                              ('speaker',speech['speaker']),
                              ('speaker_bioguide',speech['speaker_bioguide']),
                              ('pageid',crfile['id']),
                              ('text',rd(speech['text'])),
                              ('turn',speech['turn'])
                             ]) # Gotta get rid of delimiter char
                speeches.append(speech_row)

        # SPEECHES FOR THE SPEECH THRONE
        speechstack.add(speeches)
        

    def __init__(self,start,**kwargs):
        """
        BE SURE TO INCLUDE do_mode='yield' in kwargs!
        This object handles flow control for new data
        entering a Postgres database using congressionalrecord2s
        data model.

        It breaks the incoming Python dictionaries into three stacks
        of rows, one for each table in this data model.

        It writes the results to each of three flatfiles suitable for
        a bulk update through COPY.

        This is the way to minimize the number
        of transactions to the database, which we want.
        """
        kwargs['do_mode'] = 'yield'
        if 'csvpath' in kwargs:
            pass
        else:
            kwargs['csvpath'] = 'dbfiles'
        pagepath, billpath, speechpath = [
            os.path.join(kwargs['csvpath'], filename)
            for filename in ['pages.csv','bills.csv','speeches.csv']]
        self.downloader = dl(start,**kwargs)
        self.page_fields = ['pageid','title','chamber','extension',
                           'cr_day','cr_month','cr_year','num','vol',
                           'pages','wkday']
        self.bill_fields = ['congress','context',
                            'bill_type','bill_no','pageid']
        self.speech_fields = ['speechid','speaker','speaker_bioguide',
                              'pageid','text','turn']
        pagestack = crPages(pagepath,self.page_fields)
        billstack = crBills(billpath,self.bill_fields)
        speechstack = crSpeeches(speechpath,self.speech_fields)
        for crfile in self.downloader.yielded:
            doc = crfile.crdoc
            self.ingest(doc,pagestack,billstack,speechstack)
            pagestack.write()
            billstack.write()
            speechstack.write()
        

class crPages(outStack):
    pass

class crBills(outStack):
    
    def add(self,some_bills):
        self.stack.extend(some_bills)

class crSpeeches(crBills):
    pass
