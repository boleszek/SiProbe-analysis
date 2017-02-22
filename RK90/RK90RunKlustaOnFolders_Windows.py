'''
This script runs the bash command "klusta fname.prm" on all parameter files in dfold_list.
It expects that each dfold has "shank1" and "shank2" folders
'''
import os
import sys
import subprocess
sys.path.append('Z:\Code.Repository\Python\')

#=============================== CHOOSE FILE DIRECTORIES ======================#    
ddir = 'Z:\DataStores\Data\BO\SiProbe\' # data directory             
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

#=============================== RUN KLUSTA IN ALL FOLDERS ====================# 
# activate Klusta environment
# subprocess.call('source activate klusta', shell=True)

ntot = len(dfold_list)
ind = 0

for dfold in dfold_list:
    ind = ind+1
    nrem = ntot - ind
    
    dfold_temp = ddir+dfold+'/shank1'
    if os.path.exists(dfold_temp+'/'+dfold+'_shank1'+'.kwik'):
        print('Kwik file already axists... skiping...')
    else:
        print('Running Klusta '+dfold_temp+': '+str(nrem)+' folders remaining')
        os.chdir(dfold_temp)
        cmd_str = 'klusta '+dfold+'_shank1'+'.prm'
        subprocess.call(cmd_str, shell=True)
        # Note: subprocess.call automatically waits for subprocess to finish
    
    dfold_temp = ddir+dfold+'/shank2'
    if os.path.exists(dfold_temp+'/'+dfold+'_shank2'+'.kwik'):
        print('Kwik file already axists... skiping...')
    else:
        print('Running Klusta '+dfold_temp+': '+str(nrem)+' folders remaining')
        os.chdir(dfold_temp)
        cmd_str = 'klusta '+dfold+'_shank2'+'.prm'
        subprocess.call(cmd_str, shell=True)
        # Note: subprocess.call automatically waits for subprocess to finish

# deactivate Klusta environmnet when done
# subprocess.call('source deactivate klusta', shell=True)
