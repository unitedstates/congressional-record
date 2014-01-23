import os
import sys
import traceback

def initialize_logfile(dir):
    ''' returns a filelike object'''
    if not os.path.exists(dir):
        os.mkdir(dir)
    logfile = open(os.path.join(dir, 'parser.log'), 'a')
    return logfile

def get_stack_trace():
    exception_list = traceback.format_stack()
    exception_list = exception_list[:-2]
    exception_list.extend(traceback.format_tb(sys.exc_info()[2]))
    exception_list.extend(traceback.format_exception_only(sys.exc_info()[0], sys.exc_info()[1]))

    exception_str = "Traceback (most recent call last):\n"
    exception_str += "".join(exception_list)
    # Removing the last \n
    exception_str = exception_str[:-1]

    return exception_str
