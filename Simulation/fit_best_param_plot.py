# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 10:01:10 2019

@author: cbi
"""
import numpy as np
import neuronmodel as nm
from matplotlib import pyplot as plt
import os
import pickle

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

data_path = 'E:/02_AIS/Simulation/AIS/190708/fit_v2/data/fit/'

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
	with open(data_path+'dist_'+str(hl_i)+'_len_'+str(l)+'_v_vec.p', 'rb') as file:
		vec = pickle.load(file)
	bpv_len_sum[0,j], fwv_len_sum[0,j], ___ = nm.cal_velocity(vec, ['ais'])

		
for j, d in enumerate(dist_x):		
	with open(data_path+'dist_'+str(d)+'_len_'+str(ail_i)+'_v_vec.p', 'rb') as file:
		vec = pickle.load(file)
	bpv_dist_sum[0,j], fwv_dist_sum[0,j], ___ = nm.cal_velocity(vec, ['ais'])


# best param
title = 'na12_map = '+str(na12_map_i)+' na16_map = '+str(na16_map_i)+'\n\
aina12 = '+str(aina12_i)+' aina16 = '+str(aina16_i)+'\n\
na_type = '+str(na_type_i)+' aik = '+str(aik_i)+'\n\
hna = '+str(hna_i)+' hk = '+str(hk_i)+'\n\
hl = '+str(hl_i)+' ail = '+str(ail_i)
nm.show_data_fit(bpv_len_sum, fwv_len_sum, bpv_dist_sum, fwv_dist_sum, title)
#plt.savefig(save_figure_path+title.replace('\n',' ')+'.png')
#plt.close()