# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 10:01:10 2019

@author: cbi
"""
import numpy as np
import neuronmodel as nm
from matplotlib import pyplot as plt

plt.close('all')

def show_data_3d(bpv, fwv, title):	
	x = np.arange(10,70+1,10)
	y = np.arange(3,33+1,5)
	X, Y = np.meshgrid(x, y)	
	color = ['hotpink','gold','deepskyblue']
	fig = plt.figure(figsize=(8,3.5))
	ax1 = fig.add_subplot(1, 2, 1, projection='3d')
	for i, bp in enumerate(bpv):
		Z = bp	
		ax1.plot_surface(X, Y, Z, color=color[i], alpha=0.5, shade=False)
	
	fs = 11
	ax1.set_xticks(x)
	ax1.set_yticks(y)
	ax1.set_zticks(np.arange(30,90+1,20))

	ax1.set_xlabel('length ($\mu$m)')
	ax1.set_ylabel('location ($\mu$m)')
	ax1.set_zlabel('bpAP velocity($\mu$m/ms)')
	ax1.set_xticklabels(ax1.get_xticks(), fontname="Arial", fontsize=fs)
	ax1.set_yticklabels(ax1.get_yticks(), fontname="Arial", fontsize=fs)
	ax1.set_zticklabels(ax1.get_zticks(), fontname="Arial", fontsize=fs)
	ax1.view_init(20, -45)
#	ax1.set_title(title)
	
	ax2 = fig.add_subplot(1, 2, 2, projection='3d')
	for i, fw in enumerate(fwv):
		Z = fw
		ax2.plot_surface(X, Y, Z, color=color[i], alpha=0.5, shade=False)
	
	ax2.set_xticks(x)
	ax2.set_yticks(y)
	ax2.set_zticks(np.arange(150,300+1,50))
	ax2.set_xlabel('length ($\mu$m)')
	ax2.set_ylabel('location ($\mu$m)')
	ax2.set_zlabel('fAP velocity($\mu$m/ms)')
	ax2.set_xticklabels(ax2.get_xticks(), fontname="Arial", fontsize=fs)
	ax2.set_yticklabels(ax2.get_yticks(), fontname="Arial", fontsize=fs)
	ax2.set_zticklabels(ax2.get_zticks(), fontname="Arial", fontsize=fs)
	ax2.view_init(20, -45)
#	ax2.set_title(title)	
#	plt.tight_layout()



################################ type 1 ########################################
#figure_path = 'E:/02_AIS/Simulation/AIS/190708/fit_v2/figure/3d_sum/'
#file_path = 'E:/02_AIS/Simulation/AIS/190708/fit_v2/data/3d_type_1/'
#aina_x = [5000,8000,12000]
#aik_x = [3000,3000,3000]
#bpv, fwv = [], []
#for i in range(3):
#	bp, fw = nm.load_data_3d(file_path+'aina_'+str(aina_x[i])+'_aik_'+str(aik_x[i])+'_')
#	fw[fw>300] = None
#	fw[fw==0] = None
#	bpv.append(bp)
#	fwv.append(fw)
#show_data_3d(bpv, fwv, 'type1, ais_na=5000(r),8000(g),12000(b)\n ais_k=3000')
##plt.savefig(figure_path+'type_1_ais_na'+'.png')
##plt.close()
#
#aina_x = [8000,8000,8000]
#aik_x = [1000,3000,5000]
#bpv, fwv = [], []
#for i in range(3):
#	bp, fw = nm.load_data_3d(file_path+'aina_'+str(aina_x[i])+'_aik_'+str(aik_x[i])+'_')
#	fw[fw>300] = None
#	fw[fw==0] = None
#	bpv.append(bp)
#	fwv.append(fw)
#show_data_3d(bpv, fwv, 'type1, ais_k=1000(r),3000(g),5000(b)\n ais_na=8000')
##plt.savefig(figure_path+'type_1_ais_k'+'.png')
##plt.close()


################################ type 21 #######################################
#na_type_x = [21,24,3,4,5,6,7,8]
na_type_x = [7]
for na_type in na_type_x:
	figure_path = 'E:/02_AIS/Simulation/AIS/190708/fit_v2/figure/3d_sum/'
	file_path = 'E:/02_AIS/Simulation/AIS/190708/fit_v2/data/3d_type_'+str(na_type)+'/'
	aina12_x = [8000,8000,8000,5000,12000,8000,8000]
	aina16_x = [8000,5000,12000,8000,8000,8000,8000]
	aik_x    = [3000,3000,3000,3000,3000,1000,5000]
	
	aina12_x = [8000,8000,8000]
	aina16_x = [5000,8000,12000]
	aik_x    = [3000,3000,3000]
	bpv, fwv = [], []
	
	if na_type > 10:
		lb = 'type'+str(int(na_type/10))+'_map'+str(na_type%10)
	else:
		lb = 'type'+str(na_type)
		
	for i in range(3):
		bp, fw = nm.load_data_3d(file_path\
				   +lb\
				   +'_aina12_'+str(aina12_x[i])\
				   +'_aina16_'+str(aina16_x[i])\
				   +'_aik_'+str(aik_x[i])+'_')
		fw[fw>300] = None
		fw[fw==0] = None
		bpv.append(bp)
		fwv.append(fw)
	show_data_3d(bpv, fwv, lb + ', ais_na16=5000(r),8000(g),12000(b)\n ais_na12=8000, ais_k=3000')
#	plt.savefig(figure_path + lb + '_ais_na16'+'.png')
#	plt.close()
	
	aina12_x = [5000,8000,12000]
	aina16_x = [8000,8000,8000]
	aik_x    = [3000,3000,3000]
	bpv, fwv = [], []
	for i in range(3):
		bp, fw = nm.load_data_3d(file_path\
				   +lb\
				   +'_aina12_'+str(aina12_x[i])\
				   +'_aina16_'+str(aina16_x[i])\
				   +'_aik_'+str(aik_x[i])+'_')
		fw[fw>300] = None
		fw[fw==0] = None
		bpv.append(bp)
		fwv.append(fw)
	show_data_3d(bpv, fwv, lb + ', ais_na12=5000(r),8000(g),12000(b)\n ais_na16=8000, ais_k=3000')
#	plt.savefig(figure_path + lb + '_ais_na12'+'.png')
#	plt.close()
	
	aina12_x = [8000,8000,8000]
	aina16_x = [8000,8000,8000]
	aik_x    = [1000,3000,5000]
	bpv, fwv = [], []
	for i in range(3):
		bp, fw = nm.load_data_3d(file_path\
				   +lb\
				   +'_aina12_'+str(aina12_x[i])\
				   +'_aina16_'+str(aina16_x[i])\
				   +'_aik_'+str(aik_x[i])+'_')
		fw[fw>290] = None
		fw[fw==0] = None
		bpv.append(bp)
		fwv.append(fw)
	show_data_3d(bpv, fwv, lb + ', ais_k=1000(r),3000(g),5000(b)\n ais_na12=8000, ais_na16=8000')
#	plt.savefig(figure_path + lb + '_ais_k'+'.png')
#	plt.close()


