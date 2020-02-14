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

na_type_x = [3,4,5,6]
aina = 8000
aina12 = 8000
aina16 = 8000
aik = 3000
na12_map = 1
na16_map = 1
aina_x = [5000,12000]
aina12_x = [5000,12000]
aina16_x = [5000,12000]
aik_x = [1000,5000]

aina12_x = [8000,8000,8000,5000,12000,8000,8000]
aina16_x = [8000,5000,12000,8000,8000,8000,8000]
aik_x    = [3000,3000,3000,3000,3000,1000,5000]

for na_type in na_type_x:
	save_data_path = 'E:/02_AIS/Simulation/AIS/190708/fit_v2/data/3d_type_'+str(na_type)+'/'
	save_figure_path = 'E:/02_AIS/Simulation/AIS/190708/fit_v2/figure/3d_type_'+str(na_type)+'/'
	if not os.path.exists(save_data_path):
		os.makedirs(save_data_path)
	if not os.path.exists(save_figure_path):
		os.makedirs(save_figure_path)
	for p in range(7):
		bpv_sum = np.zeros([len(dist_x), len(len_x)])
		fwv_sum = np.zeros([len(dist_x), len(len_x)])
		for i,d in enumerate(dist_x):
			for j,l in enumerate(len_x):	
				file_name = 'type'+str(na_type)\
				   +'_aina12_'+str(aina12_x[p])\
				   +'_aina16_'+str(aina16_x[p])\
				   +'_aik_'+str(aik_x[p])\
				   +'_dist_'+str(d)+'_len_'+str(l)+'_v_vec.p'
				print(na_type,p,d,l)
				cell = nm.NeuronModel(hl=int(d),\
							       ail=int(l),\
								   na_type=na_type,\
								   aina12=aina12_x[p],\
								   aina16=aina16_x[p],\
								   aik=aik_x[p])
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
		with open(save_data_path+'type'+str(na_type)\
				   +'_aina12_'+str(aina12_x[p])\
				   +'_aina16_'+str(aina16_x[p])\
				   +'_aik_'+str(aik_x[p])\
				   +'_bpv.p', 'wb') as file:
			pickle.dump(bpv_sum, file)
		with open(save_data_path+'type'+str(na_type)\
				   +'_aina12_'+str(aina12_x[p])\
				   +'_aina16_'+str(aina16_x[p])\
				   +'_aik_'+str(aik_x[p])\
				   +'_fwv.p', 'wb') as file:
			pickle.dump(fwv_sum, file)
	

