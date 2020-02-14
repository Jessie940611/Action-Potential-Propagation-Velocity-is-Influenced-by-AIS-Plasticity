# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 19:38:48 2019

@author: cbi
"""


import numpy as np
import neuronmodel as nm
from matplotlib import pyplot as plt
plt.rcParams['animation.ffmpeg_path'] = 'C:/Program Files (x86)/ffmpeg-20191206-b66a800-win64-static/bin/ffmpeg.exe'
import matplotlib.animation as animation



def show_data_3d(data, flag, title, fn):	
	x = np.arange(10,70+1,10)
	y = np.arange(3,33+1,5)
	X, Y = np.meshgrid(x, y)	
	color = ['hotpink','gold','deepskyblue']
	
	fig = plt.figure(figsize=(4.5,3.5))
	ax = fig.add_subplot(111, projection='3d')
	for i, d in enumerate(data):
		Z = d	
		ax.plot_surface(X, Y, Z, color=color[i], alpha=0.5, shade=False)			
	ax.set_xlabel('length ($\mu$m)')
	ax.set_ylabel('location ($\mu$m)')
	ax.set_zlabel('velocity of '+flag+' ($\mu$m/ms)')
	if flag == 'bpAP':
		ax.set_zlim(30,100)
	else:
		ax.set_zlim(160,300)
	ax.set_title(title)

		
	def make_video(filename):
		FFMpegWriter = animation.writers['ffmpeg']
		metadata = dict(title='Movie Test', artist='Matplotlib',comment='Movie support!')
		writer = FFMpegWriter(fps=20, metadata=metadata)
		with writer.saving(fig, filename, dpi=1000):
			for angle in range(0, 360, 1):
				ax.view_init(30, angle)
				plt.draw()
				writer.grab_frame()
	
	print('making movie ' + title + '...')
	make_video('E:/02_AIS/Summary/AIS Paper/3d_simulation_data/' + fn + '.mp4')
	print('movie ' + title + 'done!')



if __name__ == "__main__":
	plt.close('all')
	na_type = 7
	lb = 'type'+str(na_type)
	
	figure_path = 'E:/02_AIS/Simulation/AIS/190708/fit_v2/figure/3d_sum/'
	file_path = 'E:/02_AIS/Simulation/AIS/190708/fit_v2/data/3d_type_'+str(na_type)+'/'
	aina12_x = [8000,8000,8000,5000,12000,8000,8000]
	aina16_x = [8000,5000,12000,8000,8000,8000,8000]
	aik_x    = [3000,3000,3000,3000,3000,1000,5000]
	
	################################ Nav 1.2 ##################################
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
	show_data_3d(bpv, 'bpAP', 'ais_na12=5000(r),8000(g),12000(b)\n ais_na16=8000, ais_k=3000', 'adjust_nav12')
	show_data_3d(fwv, 'fAP', 'ais_na12=5000(r),8000(g),12000(b)\n ais_na16=8000, ais_k=3000', 'adjust_nav12')
	#	plt.savefig(figure_path + lb + '_ais_na12'+'.png')
	#	plt.close()
	
	
	################################ Nav 1.6 ##################################
	aina12_x = [8000,8000,8000]
	aina16_x = [5000,8000,12000]
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
	show_data_3d(bpv, 'bpAP', 'ais_na16=5000(r),8000(g),12000(b)\n ais_na12=8000, ais_k=3000', 'adjust_nav16')
	show_data_3d(fwv, 'fAP', 'ais_na16=5000(r),8000(g),12000(b)\n ais_na12=8000, ais_k=3000', 'adjust_nav16')
	#	plt.savefig(figure_path + lb + '_ais_na16'+'.png')
	#	plt.close()
	
	
	################################### K #####################################
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
		fw[fw>298] = None
		fw[fw==0] = None
		bpv.append(bp)
		fwv.append(fw)
	show_data_3d(bpv, 'bpAP', 'ais_k=1000(r),3000(g),5000(b)\n ais_na12=8000, ais_na16=8000', 'adjust_k')
	show_data_3d(fwv, 'fAP', 'ais_k=1000(r),3000(g),5000(b)\n ais_na12=8000, ais_na16=8000', 'adjust_k')
	#	plt.savefig(figure_path + lb + '_ais_k'+'.png')
	#	plt.close()