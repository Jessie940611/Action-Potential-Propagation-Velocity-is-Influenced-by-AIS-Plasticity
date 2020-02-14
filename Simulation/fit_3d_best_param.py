# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 15:49:03 2019

@author: cbi
"""

import neuronmodel as nm
import numpy as np
from matplotlib import pyplot as plt 
from neuron import h
import pickle
import os


len_start = 10
len_step = 10
len_stop = 70
len_x = np.arange(len_start, len_stop+1, len_step)
dist_start = 3
dist_step = 5
dist_stop = 33
dist_x = np.arange(dist_start, dist_stop+1, dist_step)


na_type_i = 6
aina12_i = 5000   ####
aina16_i = 12000  ####
aik_i = 3000      ####
hna_i = 300
hk_i = 200
hl_i = 15
ail_i = 40
hd_i = 4

#aina12_x = [2000,5000,8000]
#aina16_x = [8000,12000,16000]
#aik_x = [1000,3000,5000]

aina12_x = [5000,2000,8000,5000,5000,5000,5000]
aina16_x = [12000,12000,12000,8000,16000,12000,12000]
aik_x = [3000,3000,3000,3000,3000,1000,5000]

save_data_path = 'E:/02_AIS/Simulation/AIS/190708/fit_v2/data/3d_best_param/'
save_figure_path = 'E:/02_AIS/Simulation/AIS/190708/fit_v2/figure/3d_best_param/'
if not os.path.exists(save_data_path):
	os.makedirs(save_data_path)
if not os.path.exists(save_figure_path):
	os.makedirs(save_figure_path)

for p in range(7):
	bpv_sum = np.zeros([len(dist_x), len(len_x)])
	fwv_sum = np.zeros([len(dist_x), len(len_x)])
	for i,d in enumerate(dist_x):
		for j,l in enumerate(len_x):
			print(p,d,l)
			file_name = 'aina12_'+str(aina12_x[p])\
			           +'_aina16_'+str(aina16_x[p])\
					   +'_aik_'+str(aik_x[p])\
					   +'_dist_'+str(d)\
					   +'_len_'+str(l)+'_'
			cell = nm.NeuronModel(hl=int(d), \
						       ail=int(l), \
							   na_type=na_type_i, \
							   aina12=aina12_x[p],\
							   aina16=aina16_x[p],\
							   aik=aik_x[p],\
							   hna = hna_i,\
							   hk = hk_i,\
							   hd = hd_i)
			stim = nm.attach_current_clamp(cell, amp=.7)
			vec = nm.set_recording_vectors(cell)
			nm.simulate()
			nm.save_vec(vec, save_data_path + file_name)
			nm.show_output(vec, save_figure_path + file_name)
			bpv_sum[i,j], fwv_sum[i,j], ___ = nm.cal_velocity(vec, ['ais'])
			cell.dend1 = None
			cell.dend2 = None
			cell.soma = None
			cell.hill = None
			cell.ais  = None
			cell.axon = None
			for sec in h.allsec():
				print(sec)	
	with open(save_data_path+'aina12_'+str(aina12_x[p])\
		                    +'_aina16_'+str(aina16_x[p])\
							+'_aik_'+str(aik_x[p])\
							+'_bpv.p', 'wb') as file:
		pickle.dump(bpv_sum, file)
	with open(save_data_path+'aina12_'+str(aina12_x[p])\
		                    +'_aina16_'+str(aina16_x[p])\
							+'_aik_'+str(aik_x[p])\
							+'_fwv.p', 'wb') as file:
		pickle.dump(fwv_sum, file)

	

