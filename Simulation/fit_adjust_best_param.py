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

save_figure_log_path = 'E:/02_AIS/Simulation/AIS/190708/fit_v2/figure/fit_sum/'

#na12_map_i = 4
#na16_map_i = 4
aina12_i = 5000
aina16_i = 12000
na_type_i = 6
aik_i = 3000
hna_i = 300 
hk_i = 200
hl_i = 15
ail_i = 40
hd_i = 4


############################### aina12_i ######################################
aina12_x = np.arange(1000,11000+1,2000)
bpv_len_sum = np.zeros([len(aina12_x), len(len_x)])
fwv_len_sum = np.zeros([len(aina12_x), len(len_x)])
bpv_dist_sum = np.zeros([len(aina12_x), len(dist_x)])
fwv_dist_sum = np.zeros([len(aina12_x), len(dist_x)])
save_data_path = 'E:/02_AIS/Simulation/AIS/190708/fit_v2/data/fit_aina12/'
save_figure_path = 'E:/02_AIS/Simulation/AIS/190708/fit_v2/figure/fit_aina12/'
if not os.path.exists(save_data_path):
	os.makedirs(save_data_path)
if not os.path.exists(save_figure_path):
	os.makedirs(save_figure_path)

for i,aina12_ii in enumerate(aina12_x):
	for j, l in enumerate(len_x):	
		print('aina12:',aina12_ii,j,l)
		cell = nm.NeuronModel(ail=int(l), \
						   na_type=na_type_i, \
#						   na12_map=na12_map_i, \
#						   na16_map=na16_map_i, \
						   aina12=aina12_ii, \
						   aina16=aina16_i, \
						   aik=aik_i,\
						   hna=hna_i,\
						   hk=hk_i,\
						   hl = hl_i,\
						   hd = hd_i)
		stim = nm.attach_current_clamp(cell, amp=.7)
		vec = nm.set_recording_vectors(cell)
		nm.simulate()
		nm.save_vec(vec, save_data_path+'aina12_'+str(aina12_ii)+'_dist_'+str(hl_i)+'_len_'+str(l)+'_')
		nm.show_output(vec, save_figure_path+'aina12_'+str(aina12_ii)+'_dist_'+str(hl_i)+'_len_'+str(l)+'_')
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
		print('aina12:',aina12_ii,j,d)
		cell = nm.NeuronModel(hl=int(d), \
						   na_type=na_type_i, \
#						   na12_map=na12_map_i, \
#						   na16_map=na16_map_i, \
						   aina12=aina12_ii, \
						   aina16=aina16_i, \
						   aik=aik_i,\
						   hna=hna_i,\
						   hk=hk_i,\
						   ail = ail_i,\
						   hd = hd_i)
		stim = nm.attach_current_clamp(cell, amp=.7)
		vec = nm.set_recording_vectors(cell)
		nm.simulate()
		nm.save_vec(vec, save_data_path+'aina12_'+str(aina12_ii)+'dist_'+str(d)+'_len_'+str(ail_i)+'_')
		nm.show_output(vec, save_figure_path+'aina12_'+str(aina12_ii)+'dist_'+str(d)+'_len_'+str(ail_i)+'_')
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
		

################################# aina16_i ####################################
aina16_x = np.arange(4000,14000+1,2000)
bpv_len_sum = np.zeros([len(aina16_x), len(len_x)])
fwv_len_sum = np.zeros([len(aina16_x), len(len_x)])
bpv_dist_sum = np.zeros([len(aina16_x), len(dist_x)])
fwv_dist_sum = np.zeros([len(aina16_x), len(dist_x)])
save_data_path = 'E:/02_AIS/Simulation/AIS/190708/fit_v2/data/fit_aina16/'
save_figure_path = 'E:/02_AIS/Simulation/AIS/190708/fit_v2/figure/fit_aina16/'
if not os.path.exists(save_data_path):
	os.makedirs(save_data_path)
if not os.path.exists(save_figure_path):
	os.makedirs(save_figure_path)

for i,aina16_ii in enumerate(aina16_x):
	for j, l in enumerate(len_x):	
		print('aina16:',aina16_ii,j,l)
		cell = nm.NeuronModel(ail=int(l), \
						   na_type=na_type_i, \
#						   na12_map=na12_map_i, \
#						   na16_map=na16_map_i, \
						   aina12=aina12_i, \
						   aina16=aina16_ii, \
						   aik=aik_i,\
						   hna=hna_i,\
						   hk=hk_i,\
						   hl = hl_i,\
						   hd = hd_i)
		stim = nm.attach_current_clamp(cell, amp=.7)
		vec = nm.set_recording_vectors(cell)
		nm.simulate()
		nm.save_vec(vec, save_data_path+'aina16_'+str(aina16_ii)+'_dist_'+str(hl_i)+'_len_'+str(l)+'_')
		nm.show_output(vec, save_figure_path+'aina16_'+str(aina16_ii)+'_dist_'+str(hl_i)+'_len_'+str(l)+'_')
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
		print('aina16:',aina16_ii,j,d)
		cell = nm.NeuronModel(hl=int(d), \
						   na_type=na_type_i, \
#						   na12_map=na12_map_i, \
#						   na16_map=na16_map_i, \
						   aina12=aina12_i, \
						   aina16=aina16_ii, \
						   aik=aik_i,\
						   hna=hna_i,\
						   hk=hk_i,\
						   ail = ail_i,\
						   hd = hd_i)
		stim = nm.attach_current_clamp(cell, amp=.7)
		vec = nm.set_recording_vectors(cell)
		nm.simulate()
		nm.save_vec(vec, save_data_path+'aina16_'+str(aina16_ii)+'dist_'+str(d)+'_len_'+str(ail_i)+'_')
		nm.show_output(vec, save_figure_path+'aina16_'+str(aina16_ii)+'dist_'+str(d)+'_len_'+str(ail_i)+'_')
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




############################### aik_i ######################################
aik_x = np.arange(1000,7000+1,1000)
bpv_len_sum = np.zeros([len(aik_x), len(len_x)])
fwv_len_sum = np.zeros([len(aik_x), len(len_x)])
bpv_dist_sum = np.zeros([len(aik_x), len(dist_x)])
fwv_dist_sum = np.zeros([len(aik_x), len(dist_x)])
save_data_path = 'E:/02_AIS/Simulation/AIS/190708/fit_v2/data/fit_aik/'
save_figure_path = 'E:/02_AIS/Simulation/AIS/190708/fit_v2/figure/fit_aik/'
if not os.path.exists(save_data_path):
	os.makedirs(save_data_path)
if not os.path.exists(save_figure_path):
	os.makedirs(save_figure_path)

for i,aik_ii in enumerate(aik_x):
	for j, l in enumerate(len_x):	
		print('aik:',aik_ii,j,l)
		cell = nm.NeuronModel(ail=int(l), \
						   na_type=na_type_i, \
#						   na12_map=na12_map_i, \
#						   na16_map=na16_map_i, \
						   aina12=aina12_i, \
						   aina16=aina16_i, \
						   aik=aik_ii,\
						   hna=hna_i,\
						   hk=hk_i,\
						   hl = hl_i,\
						   hd = hd_i)
		stim = nm.attach_current_clamp(cell, amp=.7)
		vec = nm.set_recording_vectors(cell)
		nm.simulate()
		nm.save_vec(vec, save_data_path+'aik_'+str(aik_ii)+'_dist_'+str(hl_i)+'_len_'+str(l)+'_')
		nm.show_output(vec, save_figure_path+'aik_'+str(aik_ii)+'_dist_'+str(hl_i)+'_len_'+str(l)+'_')
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
		print('aik:',aik_ii,j,d)
		cell = nm.NeuronModel(hl=int(d), \
						   na_type=na_type_i, \
#						   na12_map=na12_map_i, \
#						   na16_map=na16_map_i, \
						   aina12=aina12_i, \
						   aina16=aina16_i, \
						   aik=aik_ii,\
						   hna=hna_i,\
						   hk=hk_i,\
						   ail = ail_i,\
						   hd = hd_i)
		stim = nm.attach_current_clamp(cell, amp=.7)
		vec = nm.set_recording_vectors(cell)
		nm.simulate()
		nm.save_vec(vec, save_data_path+'aik_'+str(aik_ii)+'dist_'+str(d)+'_len_'+str(ail_i)+'_')
		nm.show_output(vec, save_figure_path+'aik_'+str(aik_ii)+'dist_'+str(d)+'_len_'+str(ail_i)+'_')
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
	
	
############################### hna_i ######################################
hna_x = np.arange(100,700+1,100)
bpv_len_sum = np.zeros([len(hna_x), len(len_x)])
fwv_len_sum = np.zeros([len(hna_x), len(len_x)])
bpv_dist_sum = np.zeros([len(hna_x), len(dist_x)])
fwv_dist_sum = np.zeros([len(hna_x), len(dist_x)])
save_data_path = 'E:/02_AIS/Simulation/AIS/190708/fit_v2/data/fit_hna/'
save_figure_path = 'E:/02_AIS/Simulation/AIS/190708/fit_v2/figure/fit_hna/'
if not os.path.exists(save_data_path):
	os.makedirs(save_data_path)
if not os.path.exists(save_figure_path):
	os.makedirs(save_figure_path)

for i,hna_ii in enumerate(hna_x):
	for j, l in enumerate(len_x):	
		print('hna:',hna_ii,j,l)
		cell = nm.NeuronModel(ail=int(l), \
						   na_type=na_type_i, \
#						   na12_map=na12_map_i, \
#						   na16_map=na16_map_i, \
						   aina12=aina12_i, \
						   aina16=aina16_i, \
						   aik=aik_i,\
						   hna=hna_ii,\
						   hk=hk_i,\
						   hl = hl_i,\
						   hd = hd_i)
		stim = nm.attach_current_clamp(cell, amp=.7)
		vec = nm.set_recording_vectors(cell)
		nm.simulate()
		nm.save_vec(vec, save_data_path+'hna_'+str(hna_ii)+'_dist_'+str(hl_i)+'_len_'+str(l)+'_')
		nm.show_output(vec, save_figure_path+'hna_'+str(hna_ii)+'_dist_'+str(hl_i)+'_len_'+str(l)+'_')
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
		print('hna:',hna_ii,j,d)
		cell = nm.NeuronModel(hl=int(d), \
						   na_type=na_type_i, \
#						   na12_map=na12_map_i, \
#						   na16_map=na16_map_i, \
						   aina12=aina12_i, \
						   aina16=aina16_i, \
						   aik=aik_i,\
						   hna=hna_ii,\
						   hk=hk_i,\
						   ail = ail_i,\
						   hd = hd_i)
		stim = nm.attach_current_clamp(cell, amp=.7)
		vec = nm.set_recording_vectors(cell)
		nm.simulate()
		nm.save_vec(vec, save_data_path+'hna_'+str(hna_ii)+'dist_'+str(d)+'_len_'+str(ail_i)+'_')
		nm.show_output(vec, save_figure_path+'hna_'+str(hna_ii)+'dist_'+str(d)+'_len_'+str(ail_i)+'_')
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
		

############################### hk_i ######################################
hk_x = np.arange(100,700+1,100)
bpv_len_sum = np.zeros([len(hk_x), len(len_x)])
fwv_len_sum = np.zeros([len(hk_x), len(len_x)])
bpv_dist_sum = np.zeros([len(hk_x), len(dist_x)])
fwv_dist_sum = np.zeros([len(hk_x), len(dist_x)])
save_data_path = 'E:/02_AIS/Simulation/AIS/190708/fit_v2/data/fit_hk/'
save_figure_path = 'E:/02_AIS/Simulation/AIS/190708/fit_v2/figure/fit_hk/'
if not os.path.exists(save_data_path):
	os.makedirs(save_data_path)
if not os.path.exists(save_figure_path):
	os.makedirs(save_figure_path)

for i,hk_ii in enumerate(hk_x):
	for j, l in enumerate(len_x):	
		print('hk:',hk_ii,j,l)
		cell = nm.NeuronModel(ail=int(l), \
						   na_type=na_type_i, \
#						   na12_map=na12_map_i, \
#						   na16_map=na16_map_i, \
						   aina12=aina12_i, \
						   aina16=aina16_i, \
						   aik=aik_i,\
						   hna=hna_i,\
						   hk=hk_ii,\
						   hl = hl_i,\
						   hd = hd_i)
		stim = nm.attach_current_clamp(cell, amp=.7)
		vec = nm.set_recording_vectors(cell)
		nm.simulate()
		nm.save_vec(vec, save_data_path+'hk_'+str(hk_ii)+'_dist_'+str(hl_i)+'_len_'+str(l)+'_')
		nm.show_output(vec, save_figure_path+'hk_'+str(hk_ii)+'_dist_'+str(hl_i)+'_len_'+str(l)+'_')
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
		print('hk:',hk_ii,j,d)
		cell = nm.NeuronModel(hl=int(d), \
						   na_type=na_type_i, \
#						   na12_map=na12_map_i, \
#						   na16_map=na16_map_i, \
						   aina12=aina12_i, \
						   aina16=aina16_i, \
						   aik=aik_i,\
						   hna=hna_i,\
						   hk=hk_ii,\
						   ail = ail_i,\
						   hd = hd_i)
		stim = nm.attach_current_clamp(cell, amp=.7)
		vec = nm.set_recording_vectors(cell)
		nm.simulate()
		nm.save_vec(vec, save_data_path+'hk_'+str(hk_ii)+'dist_'+str(d)+'_len_'+str(ail_i)+'_')
		nm.show_output(vec, save_figure_path+'hk_'+str(hk_ii)+'dist_'+str(d)+'_len_'+str(ail_i)+'_')
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



############################### hd_i ######################################
hd_x = np.arange(1,7+1,1)
bpv_len_sum = np.zeros([len(hd_x), len(len_x)])
fwv_len_sum = np.zeros([len(hd_x), len(len_x)])
bpv_dist_sum = np.zeros([len(hd_x), len(dist_x)])
fwv_dist_sum = np.zeros([len(hd_x), len(dist_x)])
save_data_path = 'E:/02_AIS/Simulation/AIS/190708/fit_v2/data/fit_hd/'
save_figure_path = 'E:/02_AIS/Simulation/AIS/190708/fit_v2/figure/fit_hd/'
if not os.path.exists(save_data_path):
	os.makedirs(save_data_path)
if not os.path.exists(save_figure_path):
	os.makedirs(save_figure_path)

for i,hd_ii in enumerate(hd_x):
	for j, l in enumerate(len_x):	
		print('hd:',hd_ii,j,l)
		cell = nm.NeuronModel(ail=int(l), \
						   na_type=na_type_i, \
#						   na12_map=na12_map_i, \
#						   na16_map=na16_map_i, \
						   aina12=aina12_i, \
						   aina16=aina16_i, \
						   aik=aik_i,\
						   hna=hna_i,\
						   hk=hk_i,\
						   hl = hl_i,\
						   hd = hd_ii)
		stim = nm.attach_current_clamp(cell, amp=.7)
		vec = nm.set_recording_vectors(cell)
		nm.simulate()
		nm.save_vec(vec, save_data_path+'hd_'+str(hd_ii)+'_dist_'+str(hl_i)+'_len_'+str(l)+'_')
		nm.show_output(vec, save_figure_path+'hd_'+str(hd_ii)+'_dist_'+str(hl_i)+'_len_'+str(l)+'_')
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
		print('hd:',hd_ii,j,d)
		cell = nm.NeuronModel(hl=int(d), \
						   na_type=na_type_i, \
#						   na12_map=na12_map_i, \
#						   na16_map=na16_map_i, \
						   aina12=aina12_i, \
						   aina16=aina16_i, \
						   aik=aik_i,\
						   hna=hna_i,\
						   hk=hk_i,\
						   ail = ail_i,\
						   hd = hd_ii)
		stim = nm.attach_current_clamp(cell, amp=.7)
		vec = nm.set_recording_vectors(cell)
		nm.simulate()
		nm.save_vec(vec, save_data_path+'hd_'+str(hd_ii)+'dist_'+str(d)+'_len_'+str(ail_i)+'_')
		nm.show_output(vec, save_figure_path+'hd_'+str(hd_ii)+'dist_'+str(d)+'_len_'+str(ail_i)+'_')
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
		
