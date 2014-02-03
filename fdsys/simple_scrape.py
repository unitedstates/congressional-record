import os

def find_fdsys(day):
    # expecting day in yyyy-mm-dd format
    year = day[:4]
    location = "source/" + year
    folder = "CREC-" + day
    url = "http://www.gpo.gov/fdsys/pkg/CREC-" + day + ".zip"
    file_path = os.path.join(location, folder)
    
    # looks to see if the file has already been downloaded
    if os.path.exists(file_path):
        return file_path
    
    try:
        print "Downloading url ", url
        contents = urllib2.urlopen(url).read()
    except:
        message = "No record retrieved for " + day
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
        file_path = os.path.join(location, folder, "html", filename)
        dest_path = os.path.join(location, folder, filename)
        os.rename(file_path, dest_path)
    # clean up empty folder
    os.rmdir(os.path.join(location, folder, "html"))
    
    return file_path
