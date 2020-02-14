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

hill_gna_start = 100
hill_gna_stop = 600
hill_gna_step = 100
hill_gna_x = np.arange(hill_gna_start, hill_gna_stop+1, hill_gna_step)
len_start = 10
len_step = 10
len_stop = 70
len_x = np.arange(len_start, len_stop+1, len_step)
dist_start = 3
dist_step = 5
dist_stop = 33
dist_x = np.arange(dist_start, dist_stop+1, dist_step)
bpv_len_sum = np.zeros([len(hill_gna_x), len(len_x)])
fwv_len_sum = np.zeros([len(hill_gna_x), len(len_x)])
bpv_dist_sum = np.zeros([len(hill_gna_x), len(dist_x)])
fwv_dist_sum = np.zeros([len(hill_gna_x), len(dist_x)])

save_data_path = 'E:/02_AIS/Simulation/AIS/190708/fit_v2/data/hna/'
save_figure_path = 'E:/02_AIS/Simulation/AIS/190708/fit_v2/figure/hna/'

for i,gna in enumerate(hill_gna_x):	
	
	for j, l in enumerate(len_x):
		print('hna:', gna, 'pS/um2; len:', l,'um;')		
		cell = nm.NeuronModel(ail=int(l), na_type=1, hna=gna)
		stim = nm.attach_current_clamp(cell, amp=.7)
		vec = nm.set_recording_vectors(cell)
		nm.simulate()
		nm.save_vec(vec, save_data_path+'hna_'+str(gna)+'_len_'+str(l)+'_')
		nm.show_output(vec, save_figure_path+'hna_'+str(gna)+'_len_'+str(l)+'_')
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
		print('hna:', gna, 'pS/um2; dist:', d,'um;')		
		cell = nm.NeuronModel(hl=int(d), na_type=1, hna=gna)
		stim = nm.attach_current_clamp(cell, amp=.7)
		vec = nm.set_recording_vectors(cell)
		nm.simulate()
		nm.save_vec(vec, save_data_path+'hna_'+str(gna)+'_dist_'+str(d)+'_')
		nm.show_output(vec, save_figure_path+'hna_'+str(gna)+'_dist_'+str(d)+'_')
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