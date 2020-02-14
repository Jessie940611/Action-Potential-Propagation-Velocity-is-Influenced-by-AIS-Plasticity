# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 19:38:48 2019

@author: cbi
"""


import numpy as np
import neuronmodel as nm
import matplotlib
from matplotlib import pyplot as plt
plt.rcParams['animation.ffmpeg_path'] = 'C:/Program Files (x86)/ffmpeg-20191206-b66a800-win64-static/bin/ffmpeg.exe'
import matplotlib.animation as animation


def plot3d(data, sfcolor, flag, title):
	fs = 11
	fig = plt.figure(figsize=(4.5,4.5))
	ax = fig.add_subplot(111, projection='3d')
	ax.plot_surface(X, Y, data, color=sfcolor, alpha=0.5, shade=False)
	#ax.plot_wireframe(X, Y, bp, color='darkgoldenrod')
	bl_x = np.array([x[length]]*7)
	bl_y = y
	bl_z = data[:,length]
	ax.plot(bl_x,bl_y,bl_z,color='black', linewidth=4, Linestyle=':')
	bl_x = x
	bl_y = np.array([y[loc]]*7)
	bl_z = data[loc,:]
	ax.plot(bl_x,bl_y,bl_z,color='black', linewidth=4)
	
	ax.set_xticks(x)
	ax.set_yticks(y)
	if flag == 'bpAP':
		ax.set_zticks(np.arange(25,75+1,10))
	else:
		ax.set_zticks(np.arange(170,290+1,30))
	ax.set_xlabel('length ($\mu$m)', fontname="Arial", fontsize=fs)
	ax.set_ylabel('location ($\mu$m)', fontname="Arial", fontsize=fs)
	ax.set_zlabel(flag + ' velocity ($\mu$m/ms)', fontname="Arial", fontsize=fs)
	ax.set_xticklabels(ax.get_xticks(), fontname="Arial", fontsize=fs)
	ax.set_yticklabels(ax.get_yticks(), fontname="Arial", fontsize=fs)
	ax.set_zticklabels(ax.get_zticks(), fontname="Arial", fontsize=fs)
	plt.title(title, fontname="Arial", fontsize=fs)
#	plt.tight_layout()
	
	#for angle in range(0, 360):
	#	ax1.view_init(30, angle)
	#	ax2.view_init(30, angle)	
	#	plt.draw()
	#	plt.pause(.001)
	
	def make_video(filename):
		FFMpegWriter = animation.writers['ffmpeg']
		metadata = dict(title='Movie Test', artist='Matplotlib',comment='Movie support!')
		writer = FFMpegWriter(fps=20, metadata=metadata)
		with writer.saving(fig, filename, dpi=1000):
			for angle in range(0, 360, 1):
				ax.view_init(15, angle)
				plt.draw()
				writer.grab_frame()
	
#	print('making movie ' + title + '...')
#	make_video('E:/02_AIS/Summary/AIS Paper/3d_simulation_data/' + title + '.mp4')
#	print('movie ' + title + 'done!')
				

def plotHeatmap(data, flag):
	fs = 11
	fig = plt.figure(figsize=(4,4))
	ax = fig.add_subplot(111)
	cmap = plt.cm.jet
	if flag == 'bpAP':
		norm = matplotlib.colors.Normalize(vmin=24, vmax=74)  
	else:
		norm = matplotlib.colors.Normalize(vmin=170, vmax=260)
	im = ax.imshow(data, cmap=cmap, norm=norm, aspect='equal',interpolation='nearest')
	plt.colorbar(im,shrink=1)
	ax.set_xticks(range(7))
#	ax.set_yticks(range(7))
	ax.set_xticklabels(['10','20','30','40','50','60','70'], fontname="Arial", fontsize=fs)
	ax.set_yticklabels(['','3','8','13','18','23','28','33'], fontname="Arial", fontsize=fs)
	ax.set_xlabel('AIS length ($\mu$m)', fontname="Arial", fontsize=fs)
	ax.set_ylabel('AIS location ($\mu$m)', fontname="Arial", fontsize=fs)
	plt.tight_layout()


def plotLine(bp, fw):
	fs = 11
	fig = plt.figure(figsize=(5,4.5))
	ytick = range(20,75,10)
	color = ['r','darkorange','gold','limegreen','deepskyblue','blueviolet','fuchsia']
		
	bp = bp.transpose()
	ax = fig.add_subplot(221)
	for i in range(len(bp)):
		plt.plot(bp[i], label = str(x[i]), linestyle='-', marker='o', \
		   color = color[i], markerfacecolor=color[i], markeredgecolor=color[i])
	ax.set_xticks(range(7))
	ax.set_yticks(ytick)
	ax.set_xticklabels(['3','8','13','18','23','28','33'], fontname="Arial", fontsize=fs)
	ax.set_yticklabels(ax.get_yticks(), fontname="Arial", fontsize=fs)
#	plt.legend(loc = 0, ncol = 4)
	ax.set_xlabel('AIS location ($\mu$m)', fontname="Arial", fontsize=fs)
	ax.set_ylabel('bp velocity ($\mu$m/ms)', fontname="Arial", fontsize=fs)
	plt.tight_layout()
	
	bp = bp.transpose()
	ax = fig.add_subplot(222)
	for i in range(len(bp)):
		plt.plot(bp[i], label = str(y[i]), linestyle='-', marker='o', \
		   color = color[i], markerfacecolor='w', markeredgecolor=color[i])
	ax.set_xticks(range(7))
	ax.set_yticks(ytick)
	ax.set_xticklabels(['10','20','30','40','50','60','70'], fontname="Arial", fontsize=fs)
	ax.set_yticklabels(ax.get_yticks(), fontname="Arial", fontsize=fs)
#	plt.legend(loc = 0, ncol = 4)
	ax.set_xlabel('AIS length ($\mu$m)', fontname="Arial", fontsize=fs)
	ax.set_ylabel('bp velocity ($\mu$m/ms)', fontname="Arial", fontsize=fs)
	plt.tight_layout()
	
	ytick = range(160,280+1,30)
	fw = fw.transpose()
	ax = fig.add_subplot(223)
	for i in range(len(fw)):
		plt.plot(fw[i], label = str(x[i]), linestyle='-', marker='o', \
		   color = color[i], markerfacecolor=color[i], markeredgecolor=color[i])
	ax.set_xticks(range(7))
	ax.set_yticks(ytick)
	ax.set_xticklabels(['3','8','13','18','23','28','33'], fontname="Arial", fontsize=fs)
	ax.set_yticklabels(ax.get_yticks(), fontname="Arial", fontsize=fs)
#	plt.legend(loc = 0, ncol = 3)
	ax.set_xlabel('AIS location ($\mu$m)', fontname="Arial", fontsize=fs)
	ax.set_ylabel('fAP velocity ($\mu$m/ms)', fontname="Arial", fontsize=fs)
	plt.tight_layout()
	
	fw = fw.transpose()
	ax = fig.add_subplot(224)
	for i in range(len(fw)):
		plt.plot(fw[i], label = str(y[i]), linestyle='-', marker='o', \
		   color = color[i], markerfacecolor='w', markeredgecolor=color[i])
	plt.plot(0,190,color='w')
	ax.set_xticks(range(7))
	ax.set_yticks(ytick)
	ax.set_xticklabels(['10','20','30','40','50','60','70'], fontname="Arial", fontsize=fs)
	ax.set_yticklabels(ax.get_yticks(), fontname="Arial", fontsize=fs)
#	plt.legend(loc = 0, ncol = 3)
	ax.set_xlabel('AIS length ($\mu$m)', fontname="Arial", fontsize=fs)
	ax.set_ylabel('fAP velocity ($\mu$m/ms)', fontname="Arial", fontsize=fs)
	plt.tight_layout()


if __name__ == "__main__":
	plt.close('all')
	
	aina12 = 8000
	aina16 = 8000
	aik    = 3000
	
	x = np.arange(10,70+1,10)
	y = np.arange(3,33+1,5)
	X, Y = np.meshgrid(x, y)
	loc = 1
	length = 2
	
	################################ type 8 #######################################
	
	na_type = 8  # 8(uniform), 7(step) 
	file_path = 'E:/02_AIS/Simulation/AIS/190708/fit_v2/data/3d_type_'+str(na_type)+'/'
	
	lb = 'type' + str(na_type)
	bp, fw = nm.load_data_3d(file_path + lb\
			   +'_aina12_'+str(aina12)\
			   +'_aina16_'+str(aina16)\
			   +'_aik_'+str(aik)+'_')
	fw[:,0] = np.nan
	fw[fw==0] = np.nan
	
	plotHeatmap(bp, 'bpAP')
	plotHeatmap(fw, 'fAP')
	plotLine(bp, fw)
	plot3d(bp,'darkgray','bpAP','Type 1 bpAP')
	plot3d(fw,'darkgray','fAP','Type 1 fAP')
	
	################################ type 7 #######################################
	
	na_type = 7  # 8(uniform), 7(step) 
	file_path = 'E:/02_AIS/Simulation/AIS/190708/fit_v2/data/3d_type_'+str(na_type)+'/'
	
	lb = 'type' + str(na_type)	
	bp, fw = nm.load_data_3d(file_path + lb\
			   +'_aina12_'+str(aina12)\
			   +'_aina16_'+str(aina16)\
			   +'_aik_'+str(aik)+'_')
#	fw[fw>300] = np.nan
	fw[:,0] = np.nan
	
	plotHeatmap(bp, 'bpAP')
	plotHeatmap(fw, 'fAP')
	plotLine(bp, fw)
	plot3d(bp,'gold','bpAP','Type 2 bpAP')
	plot3d(fw,'gold','fAP','Type 2 fAP')


