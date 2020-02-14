# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 15:49:03 2019

changing distance

@author: cbi
"""

import neuronmodel as nm
import numpy as np
from matplotlib import pyplot as plt 
from neuron import h
import os


len_start = 10
len_step = 10
len_stop = 70
len_x = np.arange(len_start, len_stop+1, len_step)
dist_start = 3
dist_step = 5
dist_stop = 33
dist_x = np.arange(dist_start, dist_stop+1, dist_step)
bpv_len_sum = np.zeros([1, len(len_x)])
fwv_len_sum = np.zeros([1, len(len_x)])
bpv_dist_sum = np.zeros([1, len(dist_x)])
fwv_dist_sum = np.zeros([1, len(dist_x)])

save_figure_path = 'E:/02_AIS/Simulation/AIS/190708/fit_v2/figure/fit/'
save_figure_log_path = 'E:/02_AIS/Simulation/AIS/190708/fit_v2/figure/fit_log/'
if not os.path.exists(save_figure_path):
	os.makedirs(save_figure_path)
if not os.path.exists(save_figure_log_path):
	os.makedirs(save_figure_log_path)

na12_map_i = 4
na16_map_i = 4
aina12_i = 5000
aina16_i = 12000
na_type_i = 6
aik_i = 3000
hna_i = 300 
hk_i = 200
hl_i = 15
ail_i = 40
hd_i = 4


for j, l in enumerate(len_x):	
	print(j,l)
	cell = nm.NeuronModel(ail=int(l), \
					   na_type=na_type_i, \
					   na12_map=na12_map_i, \
					   na16_map=na16_map_i, \
					   aina12=aina12_i, \
					   aina16=aina16_i, \
					   aik=aik_i,\
					   hna=hna_i,\
					   hk=hk_i,\
					   hl = hl_i,\
					   hd = hd_i)
	stim = nm.attach_current_clamp(cell, amp=.7)
	vec = nm.set_recording_vectors(cell)
	nm.simulate()
	nm.show_output(vec, save_figure_log_path+'len_'+str(l)+'_')
	bpv_len_sum[0,j], fwv_len_sum[0,j], ___ = nm.cal_velocity(vec, ['ais'])
	cell.dend1 = None
	cell.dend2 = None
	cell.soma = None
	cell.hill = None
	cell.ais  = None
	cell.axon = None
	for sec in h.allsec():
		print(sec)
		
for j, d in enumerate(dist_x):	
	print(j,d)	
	cell = nm.NeuronModel(hl=int(d), \
					   na_type=na_type_i, \
					   na12_map=na12_map_i, \
					   na16_map=na16_map_i, \
					   aina12=aina12_i, \
					   aina16=aina16_i, \
					   aik=aik_i,\
					   hna=hna_i,\
					   hk=hk_i,\
					   ail = ail_i,\
					   hd = hd_i)
	stim = nm.attach_current_clamp(cell, amp=.7)
	vec = nm.set_recording_vectors(cell)
	nm.simulate()
	nm.show_output(vec, save_figure_log_path+'dist_'+str(d)+'_')
	bpv_dist_sum[0,j], fwv_dist_sum[0,j], ___ = nm.cal_velocity(vec, ['ais'])
	cell.dend1 = None
	cell.dend2 = None
	cell.soma = None
	cell.hill = None
	cell.ais  = None
	cell.axon = None
	for sec in h.allsec():
		print(sec)


# best param
title = 'na12_map = '+str(na12_map_i)+' na16_map = '+str(na16_map_i)+'\n\
aina12 = '+str(aina12_i)+' aina16 = '+str(aina16_i)+'\n\
na_type = '+str(na_type_i)+' aik = '+str(aik_i)+'\n\
hna = '+str(hna_i)+' hk = '+str(hk_i)+'\n\
hl = '+str(hl_i)+' ail = '+str(ail_i)
nm.show_data_fit(bpv_len_sum, fwv_len_sum, bpv_dist_sum, fwv_dist_sum, title)
plt.savefig(save_figure_path+title.replace('\n',' ')+'.png')
#plt.close()