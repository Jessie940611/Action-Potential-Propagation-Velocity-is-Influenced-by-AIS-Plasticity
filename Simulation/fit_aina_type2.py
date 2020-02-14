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
import pickle
import os

ais_gna_start = 1000
ais_gna_stop = 8000
ais_gna_step = 1000
ais_gna_x = np.arange(ais_gna_start, ais_gna_stop+1, ais_gna_step)
len_start = 10
len_step = 10
len_stop = 70
len_x = np.arange(len_start, len_stop+1, len_step)
dist_start = 3
dist_step = 5
dist_stop = 33
dist_x = np.arange(dist_start, dist_stop+1, dist_step)

for na12m in range(1,5):
	for na16m in range(1,5):

		bpv_len_sum = np.zeros([len(ais_gna_x), len(len_x)])
		fwv_len_sum = np.zeros([len(ais_gna_x), len(len_x)])
		bpv_dist_sum = np.zeros([len(ais_gna_x), len(dist_x)])
		fwv_dist_sum = np.zeros([len(ais_gna_x), len(dist_x)])
		
		save_data_path = 'E:/02_AIS/Simulation/AIS/190708/fit_v2/data/aina'+str(na12m)+str(na16m)+'/'
		save_figure_path = 'E:/02_AIS/Simulation/AIS/190708/fit_v2/figure/aina'+str(na12m)+str(na16m)+'/'
		if not os.path.exists(save_data_path):
			os.makedirs(save_data_path)
		if not os.path.exists(save_figure_path):
			os.makedirs(save_figure_path)

		for i,gna in enumerate(ais_gna_x):		
			for j, l in enumerate(len_x):
				print('na12m:',na12m, '; na16m:',na16m, ';gna:', gna, 'pS/um2; len:', l,'um;')		
				cell = nm.NeuronModel(ail = int(l), na_type=2, na12_map=na12m, na16_map=na16m, aina12=gna, aina16=gna)
				stim = nm.attach_current_clamp(cell, amp=.7)
				vec = nm.set_recording_vectors(cell)
				nm.simulate()
				nm.save_vec(vec, save_data_path+str(na12m)+str(na16m)+'_gna_'+str(gna)+'_len_'+str(l)+'_')
				nm.show_output(vec, save_figure_path+str(na12m)+str(na16m)+'gna_'+str(gna)+'_len_'+str(l)+'_')
				bpv_len_sum[i,j], fwv_len_sum[i,j], ___ = nm.cal_velocity(vec, ['ais'])
				cell.dend1 = None
				cell.dend2 = None
				cell.soma = None
				cell.hill = None
				cell.ais  = None
				cell.axon = None
				for sec in h.allsec():
					print(sec)
					
			for j, d in enumerate(dist_x):
				print('na12m:',na12m, '; na16m:',na16m, ';gna:', gna, 'pS/um2; dist:', d,'um;')		
				cell = nm.NeuronModel(hl=int(d), na_type=2, na12_map=na12m, na16_map=na16m, aina12=gna, aina16=gna)
				stim = nm.attach_current_clamp(cell, amp=.7)
				vec = nm.set_recording_vectors(cell)
				nm.simulate()
				nm.save_vec(vec, save_data_path+str(na12m)+str(na16m)+'_gna_'+str(gna)+'_dist_'+str(d)+'_')
				nm.show_output(vec, save_figure_path+str(na12m)+str(na16m)+'_gna_'+str(gna)+'_dist_'+str(d)+'_')
				bpv_dist_sum[i,j], fwv_dist_sum[i,j], ___ = nm.cal_velocity(vec, ['ais'])
				cell.dend1 = None
				cell.dend2 = None
				cell.soma = None
				cell.hill = None
				cell.ais  = None
				cell.axon = None
				for sec in h.allsec():
					print(sec)
		
		with open(save_data_path+'bpv_len.p', 'ab') as file:
			pickle.dump(bpv_len_sum, file)
		with open(save_data_path+'fwv_len.p', 'ab') as file:
			pickle.dump(fwv_len_sum, file)
		with open(save_data_path+'bpv_dist.p', 'ab') as file:
			pickle.dump(bpv_dist_sum, file)
		with open(save_data_path+'fwv_dist.p', 'ab') as file:
			pickle.dump(fwv_dist_sum, file)