# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 10:01:10 2019

@author: cbi
"""
import numpy as np
import neuronmodel as nm
from matplotlib import pyplot as plt


figure_path = 'E:/02_AIS/Simulation/AIS/190708/fit_v2/figure/3d_sum/'
file_path = 'E:/02_AIS/Simulation/AIS/190708/fit_v2/data/3d_best_param/'
aina12_x = [5000,2000,8000,5000,5000,5000,5000]
aina16_x = [12000,12000,12000,8000,16000,12000,12000]
aik_x = [3000,3000,3000,3000,3000,1000,5000]

plt.close('all')


def show_data_3d(bpv, fwv, title):	
	x = np.arange(10,70+1,10)
	y = np.arange(3,33+1,5)
	X, Y = np.meshgrid(x, y)	
	color = ['hotpink','gold','deepskyblue']
	fig = plt.figure(figsize=plt.figaspect(0.5))
	ax1 = fig.add_subplot(1, 2, 1, projection='3d')
	for i, bp in enumerate(bpv):
		Z = bp	
		ax1.plot_surface(X, Y, Z, color=color[i], alpha=0.5, shade=False)
	
	bl_x = np.array([40]*7)
	bl_y = y
	Z = bpv[1]
	bl_z = Z[:,3]
	ax1.plot(bl_x,bl_y,bl_z,color='black', linewidth=3)
	bl_x = x
	bl_y = np.array([18]*7)
	bl_z = Z[3,:]
	ax1.plot(bl_x,bl_y,bl_z,color='black', linewidth=3)
			
	ax1.set_xlabel('length (um)')
	ax1.set_ylabel('distance (um)')
	ax1.set_zlabel('velocity of bpAP ($\mu$m/ms)')
	ax1.set_title(title)
	
	ax2 = fig.add_subplot(1, 2, 2, projection='3d')
	for i, fw in enumerate(fwv):
		Z = fw
		ax2.plot_surface(X, Y, Z, color=color[i], alpha=0.5, shade=False)
		
	Z = fwv[1]
	bl_x = np.array([40]*7)
	bl_y = y
	bl_z = Z[:,3]
	ax2.plot(bl_x,bl_y,bl_z,color='black', linewidth=3)
	bl_x = x
	bl_y = np.array([18]*7)
	bl_z = Z[3,:]
	ax2.plot(bl_x,bl_y,bl_z,color='black', linewidth=3)
	ax2.set_xlabel('length (um)')
	ax2.set_ylabel('location ($\mu$m)')
	ax2.set_zlabel('velocity of fwAP ($\mu$m/ms)')
	ax2.set_title(title)	
	plt.tight_layout()



aina12_x = [2000,5000,8000]
aina16_x = [12000,12000,12000]
aik_x    = [3000,3000,3000]
bpv, fwv = [], []	
for i in range(3):
	bp, fw = nm.load_data_3d(file_path\
			   +'aina12_'+str(aina12_x[i])\
			   +'_aina16_'+str(aina16_x[i])\
			   +'_aik_'+str(aik_x[i])+'_')
	fw[fw>300] = None
	fw[fw==0] = None
	bpv.append(bp)
	fwv.append(fw)
show_data_3d(bpv, fwv, 'ais_na12=2000(r),5000(y),8000(b)\n ais_na16=12000,ais_k=3000')
#	plt.savefig(figure_path + lb + '_ais_na16'+'.png')
#	plt.close()



aina12_x = [5000,5000,5000]
aina16_x = [8000,12000,16000]
aik_x    = [3000,3000,3000]
bpv, fwv = [], []
for i in range(3):
	bp, fw = nm.load_data_3d(file_path\
			   +'aina12_'+str(aina12_x[i])\
			   +'_aina16_'+str(aina16_x[i])\
			   +'_aik_'+str(aik_x[i])+'_')
	fw[fw>300] = None
	fw[fw==0] = None
	bpv.append(bp)
	fwv.append(fw)
show_data_3d(bpv, fwv, 'ais_na16=8000(r),12000(y),16000(b)\n ais_na12=8000, ais_k=3000')
#	plt.savefig(figure_path + lb + '_ais_na12'+'.png')
#	plt.close()



aina12_x = [5000,5000,5000]
aina16_x = [12000,12000,12000]
aik_x    = [1000,3000,5000]
bpv, fwv = [], []
for i in range(3):
	bp, fw = nm.load_data_3d(file_path\
			   +'aina12_'+str(aina12_x[i])\
			   +'_aina16_'+str(aina16_x[i])\
			   +'_aik_'+str(aik_x[i])+'_')
	fw[fw>300] = None
	fw[fw==0] = None
	bpv.append(bp)
	fwv.append(fw)
show_data_3d(bpv, fwv, 'ais_k=1000(r),3000(y),5000(b)\n ais_na12=5000, ais_na16=12000')
#	plt.savefig(figure_path + lb + '_ais_k'+'.png')
#	plt.close()



# show the best param
bp = bpv[1]
fw = fwv[1]
x = np.arange(10,70+1,10)
y = np.arange(3,33+1,5)
X, Y = np.meshgrid(x, y)

fig = plt.figure(figsize=(8,4))
ax1 = fig.add_subplot(1, 2, 1, projection='3d')
ax1.plot_surface(X, Y, bp, color='gold', alpha=0.5, shade=False)
#ax1.plot_wireframe(X, Y, bp, color='darkgoldenrod')
bl_x = np.array([40]*7)
bl_y = y
bl_z = bp[:,3]
ax1.plot(bl_x,bl_y,bl_z,color='black', linewidth=4)
bl_x = x
bl_y = np.array([18]*7)
bl_z = bp[3,:]
ax1.plot(bl_x,bl_y,bl_z,color='black', linewidth=4)
ax1.set_xlabel('length (um)')
ax1.set_ylabel('location (um)')
ax1.set_zlabel('velocity of bpAP ($\mu$m/ms)')
plt.title('best params')



ax2 = fig.add_subplot(1, 2, 2, projection='3d')
ax2.plot_surface(X, Y, fw, color='gold', alpha=0.5, shade=False)
#ax2.plot_wireframe(X, Y, fw, color='darkgoldenrod')
bl_x = np.array([40]*7)
bl_y = y
bl_z = fw[:,3]
ax2.plot(bl_x,bl_y,bl_z,color='black', linewidth=4)
bl_x = x
bl_y = np.array([18]*7)
bl_z = fw[3,:]
ax2.plot(bl_x,bl_y,bl_z,color='black', linewidth=4)
ax2.set_xlabel('length (um)')
ax2.set_ylabel('location ($\mu$m)')
ax2.set_zlabel('velocity of fwAP ($\mu$m/ms)')
plt.title('best params')
plt.tight_layout()
