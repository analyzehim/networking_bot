# -*- coding: utf-8 -*-

import socket
import time
import linecache
import cPickle
import sys
import traceback
import datetime

def human_time():
    return datetime.datetime.fromtimestamp(int(time.time())).strftime('%Y-%m-%d %H:%M:%S')

def trasform_to_human_time(timestamp):
    return datetime.datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S')


def get_exception():
    exc_type, exc_value, exc_traceback = sys.exc_info()
    lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
    return ''.join('!! ' + line for line in lines)


def get_host():
    return str(socket.getfqdn())


# def log_event(text):
#     logging.basicConfig(filename="sample.log", level=logging.INFO)
#     logging.error(text)
#     print "1111111"*20
#     with open('log.txt', 'a') as f:
#         event = '%s >> %s' % (time.ctime(), text)
#         print event + '\n'
#         f.write(event+'\n')
#     return True



