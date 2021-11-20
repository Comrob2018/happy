################################
## NAME:    Robert Hendrickson
## ID:      instructor05
## DATE:    10-07-2021
## UPDATED: 11-16-2021:21:20
## FILE:    hapy_serch.py
## VERSION: 2.0
################################
"""
This program will search a filesystem for a file using regular expressions
USAGE: 
import hapy_serch
| hapy_serch.searcher(starter, known, filename, platform)
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
    # Open the file in read binary mode
    with open(filename, 'rb') as handle:
        # store the file contents in a variable
        filecontents = handle.read()
    # Store result of hashlib md5 function in a varible
    md5_hash = hashlib.md5(filecontents)
    # return the hexdigest of the md5_hash above
    return md5_hash.hexdigest()


def searcher(starter, known, filename, platform):
    """
    This will search the file system from root for a 
    file meeting a specified regular expression, once
    found it will return the file path and a hash for
    each file.
    :platform: a string of the system platform
    :pattern: a list of regular expression patterns
    :filename: a filename provided if known
    :starter: the start location for the search
    :known: a boolean value if the file name is known 
    :returns md5 hash of files in question
    """
    # Initialize a variable to store the results
    results = []
    # This will check the for a provided start directory
    if len(starter): 
        # if none is provided it will default to root
        start = starter
    else:
        # We must check if the system platform is windows or linux
        # If it is linux then the root is /
        if platform.startswith('linux'):
            start = '/'
        # If it is windows the platform will start with win and 
        # start the search in the c drive
        elif platform.startswith('win'):
            start = 'C:\\'
    # We check if the known value is True or false
    if known: 
        # If true it uses the pattern prvided by escaping the filename/pattern
        pattern = r'^\.?'+re.escape(filename)
    else:
        # This is the default pattern if the name is unknown
        # It is a pattern to search for 3 Capital letters, dash, 2 numbers, dash, 4 numbers
        pattern = r'^\.?[A-Z]{3}-\d{2}-\d{4}'
    # Search the file system from the start provided or / 
    # for current path, directories and files in current path
    for path, directories, files in os.walk(start):
        # For the current file in the files 
        for curfile in files:
            # if the current file matches the pattern provided
            if re.findall(pattern, curfile):
                # The full path will be the current path joined with the current file
                fullpath = os.path.join(path, curfile)
                # The current result is the file name and md5 hash of the full path
                current = '{0}--HASH: {1}'.format(fullpath, md5(fullpath))
                # We append the current result to a list
                results.append(current)

    return results
