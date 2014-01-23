import os

def initialize_logfile(dir):
    ''' returns a filelike object'''
    if not os.path.exists(dir):
        os.mkdir(dir)
    logfile = open(os.path.join(dir, 'parser.log'), 'a')
    return logfile
