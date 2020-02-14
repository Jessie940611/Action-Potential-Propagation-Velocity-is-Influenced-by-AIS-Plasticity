# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 10:01:10 2019

@author: cbi
"""
import numpy as np
import neuronmodel as nm
from matplotlib import pyplot as plt

# adjusting ais_na
figure_path = 'E:/02_AIS/Simulation/AIS/190708/fit_v2/figure/sum/'
file_path = 'E:/02_AIS/Simulation/AIS/190708/fit_v2/data/aina/'
bpv_len, fwv_len, bpv_dist, fwv_dist = nm.load_data(file_path)
legt = 'ais_na'
leg = np.linspace(1000,8000,8)
nm.show_data(bpv_len, fwv_len, bpv_dist, fwv_dist, legt, leg)
#plt.savefig(figure_path+legt+'.png')
#plt.close()

# adjusting hill_na
file_path = 'E:/02_AIS/Simulation/AIS/190708/fit_v2/data/hna/'
bpv_len, fwv_len, bpv_dist, fwv_dist = nm.load_data(file_path)
legt = 'hill_na'
leg = np.linspace(100,600,6)
nm.show_data(bpv_len, fwv_len, bpv_dist, fwv_dist, legt, leg)
#plt.savefig(figure_path+legt+'.png')
#plt.close()

# adjusting gna_max
for na12m in range(1,5):
	for na16m in range(1,5):
		file_path = 'E:/02_AIS/Simulation/AIS/190708/fit_v2/data/aina'+str(na12m)+str(na16m)+'/'
		bpv_len, fwv_len, bpv_dist, fwv_dist = nm.load_data(file_path)
		legt = 'ais_na_'+str(na12m)+str(na16m)
		leg = np.linspace(1000,8000,8)
		nm.show_data(bpv_len, fwv_len, bpv_dist, fwv_dist, legt, leg)
#		plt.savefig(figure_path+legt+'.png')
#		plt.close()

# best param
file_path = 'E:/02_AIS/Simulation/AIS/190708/fit_v2/data/fit/'
bpv_len, fwv_len, bpv_dist, fwv_dist = nm.load_data(file_path)
legt = '11_na'
leg = np.linspace(9000,12000,4)
nm.show_data(bpv_len, fwv_len, bpv_dist, fwv_dist, legt, leg)
#plt.savefig(figure_path+legt+'.png')
#plt.close()

## Read data 
#file_path = r'E:\02_AIS\Simulation\AIS\190708\fit_v2\data\gna_1000_len_10_v_vec.p'
#with open(file_path, 'rb') as vec_file:
#	vec = pickle.load(vec_file)

#plt.figure()
#for index, k in enumerate(vec.keys()):
#	if index == 0:
#		continue
#	plt.plot(vec[k])
#plt.xlabel('time (ms)')
#plt.ylabel('mV')
#plt.show()
