# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 10:01:10 2019

@author: cbi
"""
import numpy as np
import neuronmodel as nm
from matplotlib import pyplot as plt

figure_path = 'E:/02_AIS/Simulation/AIS/190708/fit_v2/figure/fit_sum/'
file_path = 'E:/02_AIS/Simulation/AIS/190708/fit_v2/data/fit_'

def plot_data(legt,leg):
	data_path = file_path + legt + '/'
	bpv_len, fwv_len, bpv_dist, fwv_dist = nm.load_data(data_path)
	nm.show_data(bpv_len, fwv_len, bpv_dist, fwv_dist, legt, leg)
	plt.savefig(figure_path+legt+'.png')
	plt.close()

plot_data('aina12',np.arange(1000,11000+1,2000))
plot_data('aina16',np.arange(4000,14000+1,2000))
plot_data('aik', np.arange(1000,7000+1,1000))
plot_data('hna', np.arange(100,700+1,100))
plot_data('hk', np.arange(100,700+1,100))
plot_data('hd', np.arange(1,7+1,1))





