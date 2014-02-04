import os
import urllib2
import zipfile
from cStringIO import StringIO


def find_fdsys(day, **kwargs):
    # expecting day in yyyy-mm-dd format
    force = kwargs.get('force', False)
    year = day[:4]
    location = "source/" + year
    folder = "CREC-" + day
    url = "http://www.gpo.gov/fdsys/pkg/CREC-" + day + ".zip"
    file_path = os.path.join(location, folder)
    
    # looks to see if the file has already been downloaded
    if os.path.exists(file_path):
        if force == False:
            # uses files that have already been downloaded 
            return file_path
        else:
            # removes files from the last run
            # delete previous txt and htm files
            for f in os.listdir(file_path):
                file_location = os.path.join(file_path, f)
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

    if not os.path.exists("source"):
        os.mkdir("source")

    if not os.path.exists(location):
        os.mkdir(location)

    for record in zip_file.namelist():
        if record.endswith('htm') or record.endswith('xml'):
            print "Processing ", record
            zip_file.extract(record, location)

    #moving to source dir after extraction 
    for filename in os.listdir(os.path.join(location, folder, "html")):
        file_from = os.path.join(location, folder, "html", filename)
        dest_path = os.path.join(location, folder, filename)
        os.rename(file_from, dest_path)
    # clean up empty folder
    os.rmdir(os.path.join(location, folder, "html"))

    
    return file_path
