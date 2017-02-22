# -*- coding: utf-8 -*-
"""
Created on Tue Jul 19 12:45:10 2016

@author: boleslawosinski
"""

import sys
sys.path.append('/Volumes/kaylab/Code.Repository/Python/')

import Kwik

dirname = '/Volumes/kaylab/Data/BO/Si probe/RK90_2016-06-29_15-35-51_posneg50_30k_1min_EMB/'


# load spikes and events

# Events = Kwik.load(dirname+'experiment1.kwe')
Spks = Kwik.load(dirname+'experiment1.kwx')


# load recording dataset 0
Raw = Kwik.load(dirname+'experiment1_102.raw.kwd')



import numpy as np

# extract the waveforms from each channel into list of arrays
nch = 32 # number of channels
WFlist = [] # initialize list of waveform arrays
for i in range(nch):
    dataset_name = '/channel_groups/'+str(i)+'/waveforms_filtered'
    wf = Spks[dataset_name]
    WFlist.append([np.squeeze(wf)])
    print(i)
    
# extract the spike times from each channel into list of arrays
STlist = [] # initialize list of waveform arrays
for i in range(nch):
    dataset_name = '/channel_groups/'+str(0)+'/time_samples'
    st = Spks[dataset_name]
    STlist.append([np.squeeze(st)])
    print(i)
    

import matplotlib.pyplot as plt
plt.plot(WFlist[0])

plt.plot(yo[30:60,:].T)




yo=np.squeeze(np.array(WFlist[31]))

# perform PCA on waveforms form each channel
from matplotlib.mlab import PCA
WFpca = PCA(yo)
mo = WFpca.Y

 plt.plot(WFpca.Y)

# plot 1st two components of PCA
mo[:,1:2]

# NOTES

# how to view the contents of /channel_groups/31
test=Spks['/channel_groups/31']
for i in iter(test):
    print(i)
    # the output is:
    # recordings
    # time_samples
    # waveforms_filtered
    
list_of_item_names=Spks.items()
## The objects returned by dict.keys(), dict.values() and dict.items() are view objects.
## They provide a dynamic view on the dictionary’s entries, 
## which means that when the dictionary changes, the view reflects these changes.



x = []
y = []
z = []
for item in WFpca.Y:
 x.append(item[0])
 y.append(item[1])
 z.append(item[2])

