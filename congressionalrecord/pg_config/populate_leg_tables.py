import unicodecsv as csv
import yaml

"""
Given hardcoded output locations in auxdata, append rows to csv
Rewrite the thing to deal in unicode.
"""

def load_yaml(afile):
    with open(afile,'r') as inf:
        the_yaml = yaml.load(inf)
    return the_yaml

def parse_legislators(afile,append=False,idstart=0):
    if append:
        mode = 'ab'
    else:
        mode = 'wb'
    leg_bio = open('auxdata/leg_bio.csv',mode)
    bio_fields = ['bioguideid','dob','gender','religion','cspan',\
                  'govtrack','house_history','icpsr','lis','maplight',\
                  'opensecrets','thomas','votesmart',\
                  'washington_post','wikipedia','name_first',\
                  'name_last','official_full']
    leg_terms = open('auxdata/leg_terms.csv',mode)
    term_fields = ['idn','bioguideid','address','contact_form',\
                   'district','start','end','office','party','phone',\
                   'state','ttype','url']                   
    leg_fec = open('auxdata/leg_fec.csv',mode)
    fec_fields = ['fec_id','bioguideid']
    leg_yaml = load_yaml(afile)

    bio_writer = csv.DictWriter(leg_bio,fieldnames=bio_fields,delimiter='|',encoding='utf-8')
    term_writer = csv.DictWriter(leg_terms,fieldnames=term_fields,delimiter='|',encoding='utf-8')
    fec_writer = csv.DictWriter(leg_fec,fieldnames=fec_fields,delimiter='|',encoding='utf-8')
    idn = idstart  
    for leg in leg_yaml:
        bio_row = {}
        for inkey,outkey in [('bioguide','bioguideid'),\
                             ('cspan','cspan'),('govtrack','govtrack'),\
                             ('house_history','house_history'),\
                             ('icpsr','icpsr'),('lis','lis'),\
                             ('maplight','maplight'),\
                             ('opensecrets','opensecrets'),
                             ('thomas','thomas'),\
                             ('votesmart','votesmart'),\
                             ('washington_post','washington_post'),\
                             ('wikipedia','wikipedia')]:
             if inkey in list(leg['id'].keys()):
                 bio_row[outkey] = leg['id'][inkey]

        for inkey,outkey in [('birthday','dob'),\
                             ('gender','gender'),\
                             ('religion','religion')]:
            if inkey in list(leg['bio'].keys()):
                bio_row[outkey] = leg['bio'][inkey]

        for inkey,outkey in [('first','name_first'),\
                             ('last','name_last'),\
                             ('official_full','official_full')]:
            if inkey in list(leg['name'].keys()):
                bio_row[outkey] = leg['name'][inkey]

        bio_writer.writerow(bio_row)
        for term in leg['terms']:
            term_row = {}
            term_row['idn'] = idn
            idn += 1
            term_row['bioguideid'] = leg['id']['bioguide']
            for inkey,outkey in [('address','address'),\
                                 ('contact_form','contact_form'),\
                                 ('district','district'),\
                                 ('start','start'),\
                                 ('end','end'),\
                                 ('office','office'),\
                                 ('party','party'),\
                                 ('phone','phone'),\
                                 ('state','state'),\
                                 ('type','ttype'),\
                                 ('url','url')]:
                if inkey in list(term.keys()):
                    term_row[outkey] = term[inkey]
            term_writer.writerow(term_row)

        if 'fec' not in list(leg['id'].keys()):
            pass
        else:
            for fec in leg['id']['fec']:
                fec_row = {}
                fec_row['bioguideid'] = leg['id']['bioguide']
                fec_row['fec_id'] = fec
                fec_writer.writerow(fec_row)

    for afile in [leg_bio,leg_terms,leg_fec]:
        afile.close()

            
if __name__ == '__main__':
    import os
    assert 'congressionalrecord' in os.listdir(os.getcwd()),'running from wrong path.'
    parse_legislators('auxdata/leg/legislators-current.yaml')
    tid = 0
    with open('auxdata/leg_terms.csv','r') as inf:
        for l in inf:
            tid += 1

    past = parse_legislators('auxdata/leg/legislators-historical.yaml',append=True,idstart=tid)
