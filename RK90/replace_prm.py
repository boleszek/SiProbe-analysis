'''
This function deletes all old prm files and replaces with new
'''
import numpy as np
import subprocess
import os
import sys
# If running from Bo's Mac
# sys.path.append('/Volumes/kaylab-1/Code.Repository/Python/')
# If running from server
sys.path.append('/labs/kaylab/Code.Repository/Python/')


#=============================== CHOOSE FILE DIRECTORIES ======================#    
# If running on Bo's Mac
# ddir = '/Volumes/kaylab-1/DataStores/Data/BO/SiProbe/' # data directory             
# If running on server 
ddir = '/labs/kaylab/DataStores/Data/BO/SiProbe/' # data directory
# choose data folders where files are stored                                         
# dfold_list = 'RK90_2016-07-29_raw_30k_1min_S-Lim'                 
match_str = ['2016-07-29','2016-08-15'] # list of strs in all files of interest (usually date of exp)
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
    folderpath = ddir + dfold
    #=============================== DELETE OLD PRM FILES =========================#
    # for shank1                                                                           
    prmname1 = folderpath + '/shank1/' + dfold + '_shank1.prm'
    cmd_str = 'rm '+prmname1
    subprocess.call(cmd_str, shell=True)
    # for shank2                                                                                
    prmname2 = folderpath + '/shank2/' + dfold + '_shank2.prm'
    cmd_str = 'rm '+prmname2
    subprocess.call(cmd_str, shell=True)
    #=============================== GENERATE NEW PRM FILES =======================#    
    # Copy template prm file, edit relevant lines, produce specific prm file for each shank     

    # for shank1       
    replacements = {"'expfile'":"'"+dfold+"_shank1'",
    "'probefile.prb'":"'"+ddir+"RK90_shank1.prb'","n_channels=n":"n_channels=12"}
    with open(ddir + 'RK90_template.prm') as f, open(prmname1, 'w') as fcopy:
        for line in f:
            for oldstr, newstr in replacements.items():
                line = line.replace(oldstr,newstr)
            fcopy.write(line)

    # for shank2                                                                        
    replacements = {"'expfile'":"'"+dfold+"_shank2'",
    "'probefile.prb'":"'"+ddir+"RK90_shank2.prb'","n_channels=n":"n_channels=16"}
    with open(ddir + 'RK90_template.prm') as f, open(prmname2, 'w') as fcopy:
        for line in f:
            for oldstr, newstr in replacements.items():
                line = line.replace(oldstr,newstr)
            fcopy.write(line)
