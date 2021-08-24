#!/usr/bin/env python

import os, fnmatch
from shutil import copyfile
import glob

def copyfile_match(path, file_search):
    split_files = file_search.split('_')
    motif = split_files[4]
    print(motif)
    files_matched = glob.glob(path+"/"+"*"+motif+"*")
    #fnmatch.filter(os.listdir(path), '*'+motif+'*')
    print(type(files_matched))
    all_files = glob.glob(path+"/*")
    #copyfile(files_matched, '../data')
    for filename in all_files:
        if filename in files_matched:
            print(filename)
        else:
            continue

def main():
    copyfile_match(r'/home/mustaph/Documents/brutes/INCDR/SCP', 'in205141_G_12_226873_20210412.o')

if __name__ == '__main__':
    main()