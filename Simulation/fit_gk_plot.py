# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 10:01:10 2019

@author: cbi
"""
import numpy as np
import neuronmodel as nm
from matplotlib import pyplot as plt

## adjusting ais_k
figure_path = 'E:/02_AIS/Simulation/AIS/190708/fit_v2/figure/sum/'
#file_path = 'E:/02_AIS/Simulation/AIS/190708/fit_v2/data/aik/'
#bpv_len, fwv_len, bpv_dist, fwv_dist = nm.load_data(file_path)
#legt = 'ais_k'
#leg = np.linspace(500,3000,6)
#nm.show_data(bpv_len, fwv_len, bpv_dist, fwv_dist, legt, leg)
#plt.savefig(figure_path+legt+'.png')
#plt.close()
#
## adjusting hill_k
#file_path = 'E:/02_AIS/Simulation/AIS/190708/fit_v2/data/hk/'
#bpv_len, fwv_len, bpv_dist, fwv_dist = nm.load_data(file_path)
#legt = 'hill_k'
#leg = np.linspace(50,250,5)
#nm.show_data(bpv_len, fwv_len, bpv_dist, fwv_dist, legt, leg)
#plt.savefig(figure_path+legt+'.png')
#plt.close()

# adjusting gk
for na12m in range(1,5):
	for na16m in range(1,5):
		file_path = 'E:/02_AIS/Simulation/AIS/190708/fit_v2/data/aik'+str(na12m)+str(na16m)+'/'
		bpv_len, fwv_len, bpv_dist, fwv_dist = nm.load_data(file_path)
		legt = 'ais_k_'+str(na12m)+str(na16m)
		leg = np.linspace(500,3000,6)
		nm.show_data(bpv_len, fwv_len, bpv_dist, fwv_dist, legt, leg)
		plt.savefig(figure_path+legt+'.png')
		plt.close()

# best param
file_path = 'E:/02_AIS/Simulation/AIS/190708/fit_v2/data/fit/'
bpv_len, fwv_len, bpv_dist, fwv_dist = nm.load_data(file_path)
legt = '11_na'
leg = np.linspace(9000,12000,4)
nm.show_data(bpv_len, fwv_len, bpv_dist, fwv_dist, legt, leg)
plt.savefig(figure_path+legt+'.png')
plt.close()


