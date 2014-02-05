import os
import urllib2
import zipfile
from cStringIO import StringIO


def find_fdsys(day, **kwargs):
    # expecting day in yyyy-mm-dd format
    force = kwargs.get('force', False)
    outdir = kwargs.get('outdir')

    year = day[:4]
    here = os.path.abspath(__file__)
    directory = os.path.dirname(here) + '/..'

    location = "output/" + year
    folder = "CREC-" + day
    url = "http://www.gpo.gov/fdsys/pkg/CREC-" + day + ".zip"
    
    if outdir: 
        file_path = outdir
    else:
        file_path = os.path.join(directory, location, folder)

    
    # looks to see if the file has already been downloaded
    doc_path = os.path.join(file_path, "__text")
    if os.path.exists(doc_path):
        if force == False:
            # uses files that have already been downloaded 
            return file_path
        else:
            # removes files from the last run
            # delete previous txt and htm files
            for f in os.listdir(file_path):
                file_location = os.path.join(file_path, "__text", f)
                if os.path.isfile(file_location): 
                    os.remove(file_location)
            # delete previous log
            log_path = os.path.join(file_path, "__log")
            if os.path.exists(log_path):
                print os.listdir(log_path)
                for f in os.listdir(log_path):
                    file_location = os.path.join(log_path, f)
                    os.remove(file_location)
            # delete previous parsed results
            parsed_path = os.path.join(file_path, "__parsed")
            if os.path.exists(parsed_path):
                for f in os.listdir(parsed_path):
                    file_location = os.path.join(parsed_path, f)
                    if os.path.isfile(file_location):
                        os.remove(file_location)
    
    try:
        print "Downloading url ", url
        contents = urllib2.urlopen(url).read()
    except:
        message = "No record retrieved for %s. Attempted to download records from :%s " %(day, url)
        print message
        return None
    
    zip_file = zipfile.ZipFile(StringIO(contents))

    if not os.path.exists("output"):
        os.mkdir("output")

    if not os.path.exists(location):
        os.mkdir(location)

    for record in zip_file.namelist():
        if record.endswith('htm') or record == 'mods.xml':
            zip_file.extract(record, location)
    print "processed zip", '\n'

    files = os.path.join(file_path, "__text")
    os.mkdir(files)

    for filename in os.listdir(os.path.join(location, folder, "html")):
        file_from = os.path.join(file_path, "html", filename)
        dest_path = os.path.join(file_path, "__text", filename)
        os.rename(file_from, dest_path)
    # clean up empty folder
    os.rmdir(os.path.join(file_path, "html"))

    doc_path = os.path.join(file_path, "__text")
    print doc_path, "doc_path", '\n'
    return doc_path

