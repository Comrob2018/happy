# Name: MSgt Robert Hendrickson
# ID:   instructor05
# Date: 7 Oct 2021
"""
This program will search a filesystem for a file using regular expressions
USAGE: ~$ python3 ExpressiveSearch.py -or- import ExpressiveSearch
re module used for regular expression matching
os module used for path joining
hashlib module required to make a md5 hash file path to send to server
"""
import re
import os
import hashlib

def md5(filename):
    """
    This will take in a filename and provide the 
    md5 hash of the filecontents
    :filename: name of file
    :handle: variable for file object
    :filecontents: the contents of the file object
    :md5_hash: the results of the hashlib.md5() function
    :returns a hexdigest of the file contents provided
    """
    with open(filename, 'rb') as handle:
        filecontents = handle.read()
    md5_hash = hashlib.md5(filecontents)
    return md5_hash.hexdigest()

def searcher(starter, known, filename):
    """
    This will search the file system from root for a 
    file meeting a specified regular expression, once
    found it will return the file path and a hash for
    each file.
    :pattern: a list of regular expression patterns
    :filename: a filename provided if known
    :starter: the start location for the search
    :known: a boolean value if the file name is known 
    :returns md5 hash of files in question
    """
    results = []
    if len(starter): 
        # This will check the for a provided start directory
        # if none is provided it will default to root
        start = starter
    else: 
        start = '/'
    if known: 
        pattern = r'^\.?'+re.escape(filename)
        # pattern to search for a specific file
    else:
        pattern = r'^\.?[A-Z]{3}-\d{2}-\d{4}'
        # pattern to search for 3 Capital letters, dash, 2 #, dash, 4 #
    
    for path, _, files in os.walk(start):
        for curfile in files:
            if re.findall(pattern, curfile):
                fullpath = os.path.join(path, curfile)
                current = '{0}--HASH: {1}'.format(fullpath, md5(fullpath))
                results.append(current)

    return str(results)


#searcher(filename)
