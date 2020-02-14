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

hill_gk_start = 50
hill_gk_stop = 250
hill_gk_step = 50
hill_gk_x = np.arange(hill_gk_start, hill_gk_stop+1, hill_gk_step)
len_start = 10
len_step = 10
len_stop = 70
len_x = np.arange(len_start, len_stop+1, len_step)
dist_start = 3
dist_step = 5
dist_stop = 33
dist_x = np.arange(dist_start, dist_stop+1, dist_step)
bpv_len_sum = np.zeros([len(hill_gk_x), len(len_x)])
fwv_len_sum = np.zeros([len(hill_gk_x), len(len_x)])
bpv_dist_sum = np.zeros([len(hill_gk_x), len(dist_x)])
fwv_dist_sum = np.zeros([len(hill_gk_x), len(dist_x)])

save_data_path = 'E:/02_AIS/Simulation/AIS/190708/fit_v2/data/hk/'
save_figure_path = 'E:/02_AIS/Simulation/AIS/190708/fit_v2/figure/hk/'
if not os.path.exists(save_data_path):
	os.makedirs(save_data_path)
if not os.path.exists(save_figure_path):
	os.makedirs(save_figure_path)

for i,gk in enumerate(hill_gk_x):		
	for j, l in enumerate(len_x):
		print('hk:', gk, 'pS/um2; len:', l,'um;')		
		cell = nm.NeuronModel(ail=int(l), na_type=1, hk=gk)
		stim = nm.attach_current_clamp(cell, amp=.7)
		vec = nm.set_recording_vectors(cell)
		nm.simulate()
		nm.save_vec(vec, save_data_path+'hk_'+str(gk)+'_len_'+str(l)+'_')
		nm.show_output(vec, save_figure_path+'hk_'+str(gk)+'_len_'+str(l)+'_')
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
		print('hk:', gk, 'pS/um2; dist:', d,'um;')		
		cell = nm.NeuronModel(hl=int(d), na_type=1, hk=gk)
		stim = nm.attach_current_clamp(cell, amp=.7)
		vec = nm.set_recording_vectors(cell)
		nm.simulate()
		nm.save_vec(vec, save_data_path+'hk_'+str(gk)+'_dist_'+str(d)+'_')
		nm.show_output(vec, save_figure_path+'hk_'+str(gk)+'_dist_'+str(d)+'_')
		bpv_dist_sum[i,j], fwv_dist_sum[i,j], ___ = nm.cal_velocity(vec, ['ais'])
		cell.dend1 = None
		cell.dend2 = None
		cell.soma = None
		cell.hill = None
		cell.ais  = None
		cell.axon = None
		for sec in h.allsec():
			print(sec)

with open(save_data_path+'bpv_len.p', 'wb') as file:
	pickle.dump(bpv_len_sum, file)
with open(save_data_path+'fwv_len.p', 'wb') as file:
	pickle.dump(fwv_len_sum, file)
with open(save_data_path+'bpv_dist.p', 'wb') as file:
	pickle.dump(bpv_dist_sum, file)
with open(save_data_path+'fwv_dist.p', 'wb') as file:
	pickle.dump(fwv_dist_sum, file)