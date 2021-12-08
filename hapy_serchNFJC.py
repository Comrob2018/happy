# NAME: Robert Hendrickson
# ID:   instructor05
# DATE: 10-07-2021

import re
import os
import hashlib


def md5(filename):
    with open(filename, 'rb') as handle:
        filecontents = handle.read()
    md5_hash = hashlib.md5(filecontents)
    return md5_hash.hexdigest()


def searcher(starter, known, filename, platform):
    results = []
    if len(starter): 
        start = starter
    else:
        if platform.startswith('linux'):
            start = '/'
        elif platform.startswith('win'):
            start = 'C:\\'
    if known: 
        pattern = r'^\.?'+re.escape(filename)
    else:
        pattern = r'^\.?[A-Z]{3}-\d{2}-\d{4}'
    for path, _, files in os.walk(start):
        for curfile in files:
            if re.findall(pattern, curfile):
                fullpath = os.path.join(path, curfile)
                current = '{0}--HASH: {1}'.format(fullpath, md5(fullpath))
                results.append(current)

    return results
