'''
This script does the following:                                                   
    - Loads LFP data, subsamples at 10x, saves in flat binary format
    - Loads, rearanges, and saves high pass data in flat binary format for later clustering
        with Klusta                                                                          
    - Prepares prm file


Notes                                                                             
    - Continuous low pass data files have source 102 (1 per session)                  
    - Continuous high pass data files have source 103 (32 per session)                
    - Data and prm files for each shank are saved seperately in subfolders shank1 & shank2
'''

import numpy as np
import os
import sys
# If running on Bo's Mac
# sys.path.append('/Volumes/kaylab-1/Code.Repository/Python/')
# If running on server
sys.path.append('/labs/kaylab/Code.Repository/Python/')

import OpenEphys

#=================== SET PARAMS & CHOOSE FILE DIRECTORIES ======================#

spk_direction = 'negative'
shank1_fname = 'shank1CMR'
shank2_fname = 'shank2CMR'

# set digital referencing
# options are 'avg', 'median', or None
ref_choice = 'median'

# use channels ordered by intan headstage!!!                                                         
# must add +1 to all ch because OpenEphys does not index with 0!!!                                  
# shnk1chan = [6, 8, 7, 9, 12, 14, 1, 2, 10, 16, 4, 13, 5, 15, 3, 11]                               
# shnk1chan = [19, 18, 25, 24, 20, 17, 23, 31, 27, 32, 26, 30]                                      
shnk1chan = [22, 21, 28, 29, 19, 18, 25, 24, 20, 17, 23, 31, 27, 32, 26, 30]# all channels
shnk2chan = [12, 5, 4, 14, 15, 13, 16, 2, 6, 1, 3]# 11 channels

# if running on Bo's Mac
# ddir = '/Volumes/kaylab-1/DataStores/Data/BO/SiProbe/' # data directory           
# If running on server
ddir = '/labs/kaylab/DataStores/Data/BO/SiProbe/'  

# choose data folders where files are stored                                         
# dfold_list = 'RK90_2016-07-29_raw_30k_1min_S-Lim'                 
# match_str = ['2016-07-29','2016-08-15'] # list of strs in all files of interest (usually date of exp)
match_str = ['Spikes_6EMB-SLim-Ger']
dfold_list = []
ddir_list = os.listdir(ddir)
for file in ddir_list:
    for i in range(len(match_str)):
        if match_str[i] in file:
            dfold_list.append(file)
            
#==============================================================================#    
ntot = len(dfold_list)
ind = 0

for dfold in dfold_list:
    ind = ind+1
    nrem = ntot - ind
    print('Converting '+dfold+': '+str(nrem)+' remaining')

    folderpath = ddir + dfold # folderpath where data is stored 
    
    #=============== SUBSAMPLE LOWPASS (LFP) SIGNAL AND CONVERT TO DAT ===========#
    lfpname = '102_CH2.continuous'
    filepath = ddir + dfold + '/' + lfpname
    LFP = OpenEphys.loadContinuous(filepath, dtype=float)
    LFP = LFP['data']
    ssLFP = LFP[::10].copy() #subsampled LFP
    # save as dat file
    datnameLFP = dfold + '_LFP.dat'
    ssLFP.tofile(os.path.join(folderpath,datnameLFP))
    #==============================================================================#
    
    #======================== CONVERT HIGHPASS SIGNALS TO DAT ======================#
    # Load highpass signals of each sahnk in geometric order (bottom of shank to top)   
    # then save to flat binary file                                                                             

    # create shank1 and shank2 folders                     
    os.makedirs(folderpath + '/' + shank1_fname)
    os.makedirs(folderpath + '/' + shank2_fname)
    
    # use the folder name and shank name to name individual dat files                                  
    datname1 = dfold + '_' + shank1_fname + '.dat'
    OpenEphys.pack_2_BoMod(folderpath, filename = shank1_fname + '/' + datname1, source = '103',
                     channels = shnk1chan, dref=ref_choice)

    datname2 = dfold + '_' + shank2_fname + '.dat'
    OpenEphys.pack_2_BoMod(folderpath, filename = shank2_fname + '/' + datname2, source = '103',
                     channels = shnk2chan, dref=ref_choice)

    #==============================================================================#    

    #=============================== GENERATE NEW PRM FILES =======================#    
    # Copy template prm file, edit relevant lines, produce specific prm file for each shank     

    # for shank1                                                                        
    prmname1 = folderpath + '/' + shank1_fname + '/' + dfold + '_' + shank1_fname + '.prm'
    replacements = {"'expfile.dat'":"'"+datname1+"'",
    "'probefile.prb'":"'"+ddir+"RK90_shank1.prb'","n_channels=n":"n_channels=16",
    "detect_spikes='negative'":"detect_spikes='" + spk_direction + "'"}
    with open(ddir + 'template.prm') as f, open(prmname1, 'w') as fcopy:
        for line in f:
            for oldstr, newstr in replacements.items():
                line = line.replace(oldstr,newstr)
            fcopy.write(line)

    # for shank2                                                                        
    prmname2 = folderpath + '/' + shank2_fname + '/' + dfold + '_' + shank2_fname + '.prm'
    replacements = {"'expfile.dat'":"'"+datname2+"'",
    "'probefile.prb'":"'"+ddir+"RK90_shank2.prb'","n_channels=n":"n_channels=11",
    "detect_spikes='negative'":"detect_spikes='" + spk_direction + "'"}
    with open(ddir + 'template.prm') as f, open(prmname2, 'w') as fcopy:
        for line in f:
            for oldstr, newstr in replacements.items():
                line = line.replace(oldstr,newstr)
            fcopy.write(line)
