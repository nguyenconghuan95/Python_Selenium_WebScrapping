#!/usr/bin/python

import sys, re, os, glob

import datetime
import tempfile
import unicodedata

def is_dir(d):
    return os.path.isdir(d)

def dir_files(d, fn='*'):
    os.chdir(d)
    return glob.glob(fn)

def check_dir_exist(d):
    if not is_dir(d):
        exit("{} is not exist!!!".format(d))

def is_file_exist(fn):
    return os.path.isfile(fn)

def is_write_access(fn):
    return os.access(fn, os.W_OK)

def is_read_access(fn):
    return os.access(fn, os.R_OK)

def utf_encode(s):
    return s.encode('utf-8')

def write_file(fn, txt):
    handler = open(fn, "w")
    handler.write(utf_encode(txt))
    handler.close()
    return txt

def ENV(var):
    return os.environ.get(var)

def hex_to_dec(s):
    if (s is None) or (re.sub(r'[\s\t]', '', s) is ''):
        return None
    s = re.sub(r'0x', '', s)
    s = re.sub(r"^[0-9+]*'h", '', s)
    s = re.sub(r'\'', '', s)
    s = re.sub(r'_', '', s)
    s = re.sub(r'\s.*$', '', s)
    s = re.sub(r'h$', '', s)
    if is_hex_value(s):
        return int(s, 16)
    else:
        return None

def hexs_to_decs(arr):
    if arr is None:
        return None
    return map(hex_to_dec, arr)

def dec_to_bin(i, size):
    return format(i, ('0>%sb' % size))

def is_hex_value(s):
    hexpattern = re.compile("^[0x'h]*[0-9a-fA-F_]")
    return hexpattern.match(s)

def unicode_to_str(s):
    return unicodedata.normalize('NFKD', s).encode('ascii', 'ignore')
