# script to remove .dat from .kwik filenames
import re
import numpy as np
import os
import sys

shank1_fname = 'shank1CMR'
shank2_fname = 'shank2CMR'

ddir = '/labs/kaylab/DataStores/Data/BO/SiProbe/'  

# choose data folders where files are stored                                         
match_str = ['2016-07-29_raw','2016-08-15_raw','2016-09-11_raw','2016-09-14_raw','2016-09-29_raw','2016-10-31_raw','2016-11-12_raw']
dfold_list = []
ddir_list = os.listdir(ddir)
for file in ddir_list:
    for i in range(len(match_str)):
        if match_str[i] in file:
            dfold_list.append(file)
            
for dfold in dfold_list:
    
    folderpath = ddir + dfold # folderpath where data is stored 
    
    # shank1 kwik
    sublist = os.listdir(folderpath + '/2017/' + shank1_fname + '/')
    for subfile in sublist:
        if '.kwik' in subfile:
            kwikfile = subfile
    newkwikfile = re.sub(r".dat", "", kwikfile)
    os.rename(folderpath + '/2017/' + shank1_fname + '/' + kwikfile, 
         folderpath + '/2017/' + shank1_fname + '/' + newkwikfile)
    
    # shank1 kwx
    for subfile in sublist:
        if '.kwx' in subfile:
            kwxfile = subfile
    newkwxfile = re.sub(r".dat", "", kwxfile)
    os.rename(folderpath + '/2017/' + shank1_fname + '/' + kwxfile, 
         folderpath + '/2017/' + shank1_fname + '/' + newkwxfile)
    
    # shank2 kwik
    sublist = os.listdir(folderpath + '/2017/' + shank2_fname + '/')
    for subfile in sublist:
        if '.kwik' in subfile:
            kwikfile = subfile
    newkwikfile = re.sub(r".dat", "", kwikfile)
    os.rename(folderpath + '/2017/' + shank2_fname + '/' + kwikfile, 
         folderpath + '/2017/' + shank2_fname + '/' + newkwikfile)
    
    # shank2 kwk
    for subfile in sublist:
        if '.kwx' in subfile:
            kwxfile = subfile
    newkwxfile = re.sub(r".dat", "", kwxfile)
    os.rename(folderpath + '/2017/' + shank2_fname + '/' + kwxfile, 
         folderpath + '/2017/' + shank2_fname + '/' + newkwxfile)
    