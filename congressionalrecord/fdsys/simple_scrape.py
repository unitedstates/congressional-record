import os
import urllib2
import zipfile
from cStringIO import StringIO


def find_fdsys(day, **kwargs):
    # expecting day in yyyy-mm-dd format
    force = kwargs.get('force', False)

    # establish output directory, can be user provided, defaults to /output
    # if user provided, expected to be absolute
    outdir = kwargs.get('outdir')
    if not outdir:
        raise ValueError('output directory is required')

    if not os.path.exists(outdir):
        os.mkdir(outdir)

    # make sure the year dir is made
    year = day[:4]
    outdir_year = os.path.join(outdir, year)
    if not os.path.exists(outdir_year):
        os.mkdir(outdir_year)

    # establish path to folder that day's output will live in
    crecfolder = "CREC-" + day
    outdir_year_crecfolder = os.path.join(outdir_year, crecfolder)


    # looks to see if the file has already been downloaded
    outdir_year_crecfolder_text = os.path.join(outdir_year_crecfolder, "__text")

    if os.path.exists(outdir_year_crecfolder_text) and not force:
        print "\n Downloading from cache \n"
        return outdir_year_crecfolder_text


    if os.path.exists(outdir_year_crecfolder_text):
        # removes files from the last run
        # delete previous txt and htm files
        for f in os.listdir(outdir_year_crecfolder):
            file_location = os.path.join(outdir_year_crecfolder_text, f)
            if os.path.isfile(file_location):
                os.remove(file_location)
        # delete previous log
        log_path = os.path.join(outdir_year_crecfolder, "__log")
        if os.path.exists(log_path):
            print os.listdir(log_path)
            for f in os.listdir(log_path):
                file_location = os.path.join(log_path, f)
                os.remove(file_location)
        # delete previous parsed results
        parsed_path = os.path.join(outdir_year_crecfolder, "__parsed")
        if os.path.exists(parsed_path):
            for f in os.listdir(parsed_path):
                file_location = os.path.join(parsed_path, f)
                if os.path.isfile(file_location):
                    os.remove(file_location)

    url = "http://www.gpo.gov/fdsys/pkg/CREC-" + day + ".zip"
    try:
        print "Downloading url ", url
        contents = urllib2.urlopen(url).read()
    except:
        message = "No record retrieved for %s. Attempted to download records from :%s " %(day, url)
        print message
        return None

    zip_file = zipfile.ZipFile(StringIO(contents))
    for record in zip_file.namelist():
        if record.endswith('htm') or record == 'mods.xml':
            zip_file.extract(record, outdir_year)
    print "processed zip", '\n'

    if not os.path.exists(outdir_year_crecfolder_text):
        os.mkdir(outdir_year_crecfolder_text)

    # this works for standard download but not
    for filename in os.listdir(os.path.join(outdir_year_crecfolder, "html")):
        print filename
        file_from = os.path.join(outdir_year_crecfolder, "html", filename)
        print "from- ", file_from
        dest_path = os.path.join(outdir_year_crecfolder_text, filename)
        print "to- ", dest_path
        os.rename(file_from, dest_path)
    # clean up empty folder
    os.rmdir(os.path.join(outdir_year_crecfolder, "html"))

    print outdir_year_crecfolder_text, "doc_path", '\n'
    return outdir_year_crecfolder_text

