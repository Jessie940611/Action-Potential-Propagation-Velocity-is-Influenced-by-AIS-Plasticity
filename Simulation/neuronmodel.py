
import neuron
from neuron import h, gui
from matplotlib import pyplot as plt
import numpy as np
import pickle
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.collections import PolyCollection
from matplotlib import colors as mcolors
# somatic cell


class NeuronModel(object):
	# A standard neuron: includes dend, soma, hill, AIS, axon
	# passive and active properties
	def __init__(self, dl=1000, dd=2, sl=40, sd=20, hl=10, hd=2, ail=50, aid=1.2, axl=1000, axd=1.2,\
                  dna=100, sna=100, hna=300, aina=5000, axna=300, dk=20, sk=20, hk=150, aik=1000, axk=150,\
				  na_type=2, na12_map=1, na16_map=1, aina12=5000, aina16=5000):
		self.create_sections()		
		self.define_geometry(dl, dd, sl, sd, hl, hd, ail, aid, axl, axd)
		self.build_topology()
		self.define_biophysics(na_type, dna, sna, hna, aina, axna, dk, sk, hk, aik, axk,\
						 na12_map, na16_map, aina12, aina16)

	def create_sections(self):
		# Create the section of the neuron
		self.dend1 = h.Section(name='dend1', cell=self)
		self.soma = h.Section(name='soma', cell=self)
		self.hill = h.Section(name='hill', cell=self)
		self.ais  = h.Section(name='ais',  cell=self)
		self.axon = h.Section(name='axon', cell=self)

#		for sec in h.allsec():
#		    print(sec)

	def build_topology(self):
		# Connect the sections of the neuron
		#    param cell_type: 'somatic', 'dendritic'		
		self.soma.connect(self.dend1(1))
		self.hill.connect(self.soma(0.5))
		self.ais.connect(self.hill(1))	
		self.axon.connect(self.ais(1))
#		for s in h.allsec():
#			print(h.secname())

	def define_geometry(self, dl, dd, sl, sd, hl, hd, ail, aid, axl, axd):
		# Set the geometry of the neuron		
		self.dend1.L = self.dend1.nseg = dl   # microns
		self.dend1.diam = dd
		self.soma.L = self.soma.nseg = sl
		self.soma.diam = sd
		self.hill.L = self.hill.nseg = hl
		self.hill.diam = hd
		self.ais.L = self.ais.nseg = ail
		self.ais.diam = aid
		self.axon.L = self.axon.nseg = axl
		self.axon.diam = axd
		h.define_shape()  # translate into 3D points

	def define_biophysics(self, na_type, dna, sna, hna, aina, axna, dk, sk, hk, aik, axk,\
					   na12_map, na16_map, aina12, aina16):
		# Assign the membrane properties across the cell
		#     param na_type: 1 - add one na channel; 2 - add na1.2 and na1.6
		#     param na12/16_map: 1 - 起始端结尾端浓度不变，分布梯度改变，总量改变
		#                        2 - 分布梯度不变，总量改变（偏多）
		#                        3 - 分布梯度不变，总量改变（偏少）
		#                        4 - 总量不变，分布梯度不变

#		neuron.load_mechanisms('E://02_AIS//Simulation//AIS//190708//s_vs_d')
		
		# passive properties
		pas_g = 1/10000
		pas_e = -65
		for sec in h.allsec():
			sec.Ra = 300      # Axial resistance in Ohm * cm
			sec.cm = 0.5      # Membrane capacitance in micro Farads / cm^2
			sec.insert('pas')
		secset = [self.dend1, self.soma, self.hill, self.ais, self.axon]
		secset2 = [self.dend1, self.soma, self.hill, self.axon]
		for sec in secset:
			for seg in sec:
				seg.pas.g = pas_g    # mho/cm2
				seg.pas.e = pas_e
		
		# active properties -- dend1, dend2, soma, hill, axon
		na = [dna, dna, sna, hna, axna]
		k = [dk, dk, sk, hk, axk]
		for i, sec in enumerate(secset2):
			sec.insert('naDF')
			sec.insert('kvDF')
			for seg in sec:
				seg.naDF.gbar = na[i]
				seg.kvDF.gbar = k[i]
		
		# active properties -- ais
		if na_type == 1:
			self.ais.insert('naDF')
			self.ais.insert('kvDF')				
			for seg in self.ais:
				seg.naDF.gbar = aina
				seg.kvDF.gbar = aik

		elif na_type == 2:
			self.ais.insert('na12')
			self.ais.insert('na16')
			self.ais.insert('kvDF')
			num = self.ais.nseg
			maxnum = 70
			if num > maxnum:
				return 0
			
			# define na12 density
			if na12_map == 1:
				na12 = np.linspace(aina12, aina12*0.2, num)
			elif na12_map == 2:
				temp = np.linspace(aina12, aina12*0.2, maxnum)
				na12 = temp[0:num]
			elif na12_map == 3:
				temp = np.linspace(aina12, aina12*0.2, maxnum)
				na12 = temp[maxnum-num:]
			elif na12_map == 4:
				temp = np.linspace(aina12, aina12*0.2, maxnum)
				etr = np.sum(temp[num:])
				inc = float(etr)/num
				na12 = temp[0:num] + inc
			
			# define na16 density
			if na16_map == 1:
				na16 = np.linspace(aina16*0.2, aina16, num)
			elif na16_map == 2:
				temp = np.linspace(aina16*0.2, aina16, maxnum)
				na16 = temp[maxnum-num:]
			elif na16_map == 3:
				temp = np.linspace(aina16*0.2, aina16, maxnum)
				na16 = temp[0:num]
			elif na16_map == 4:
				temp = np.linspace(aina16*0.2, aina16, maxnum)
				etr = np.sum(temp[0:maxnum-num])
				inc = float(etr)/num
				na16 = temp[maxnum-num:] + inc
		
			for i,seg in enumerate(self.ais):
				seg.na12.gbar = na12[i]
				seg.na16.gbar = na16[i]
				seg.kvDF.gbar = aik
				
		elif na_type == 3:
			self.ais.insert('na12')
			self.ais.insert('na16')
			self.ais.insert('kvDF')
			num = self.ais.nseg
			xmax = 105
			na12_map = np.flipud(np.linspace(aina12*0.2, aina12, xmax))
			na16_map = np.linspace(aina16*0.2, aina16, xmax)
			map_s = self.hill.nseg
			for i,seg in enumerate(self.ais):
				seg.na12.gbar = na12_map[map_s+i]
				seg.na16.gbar = na16_map[map_s+i]
				seg.kvDF.gbar = aik

		elif na_type == 4:
			self.ais.insert('na12')
			self.ais.insert('na16')
			self.ais.insert('kvDF')
			num = self.ais.nseg
			na12_map = np.hstack((np.linspace(aina12*0.2, aina12, round(num*0.2)),
						  np.flipud(np.linspace(aina12*0.2, aina12, round(num*0.8)))))
			na16_map = np.hstack((np.linspace(aina16*0.2, aina16, round(num*0.8)),
						  np.flipud(np.linspace(aina16*0.2, aina16, round(num*0.2)))))
			for i,seg in enumerate(self.ais):
				seg.na12.gbar = na12_map[i]
				seg.na16.gbar = na16_map[i]
				seg.kvDF.gbar = aik
							
		elif na_type == 5:
			self.ais.insert('na12')
			self.ais.insert('na16')
			self.ais.insert('kvDF')
			num = self.ais.nseg
			na12_map = np.hstack(( np.array([aina12]*round(num*0.3)),
						 np.array([aina12*0.2]*round(num*0.7))))
			na16_map = np.hstack(( np.array([aina16*0.2]*round(num*0.7)),
						 np.array([aina16]*round(num*0.3))))
			for i,seg in enumerate(self.ais):
				seg.na12.gbar = na12_map[i]
				seg.na16.gbar = na16_map[i]
				seg.kvDF.gbar = aik

		elif na_type == 6:
			self.ais.insert('na12')
			self.ais.insert('na16')
			self.ais.insert('kvDF')
			num = self.ais.nseg
			na12_map = np.hstack((np.array([aina12*0.2]*2), 
						 np.array([aina12]*3),
						 np.array([aina12*0.2]*(num-2-3))))
			na16_map = np.hstack((np.array([aina16*0.2]*(num-2-3)),
						 np.array([aina16]*3),
						 np.array([aina16*0.2]*2)))
			for i,seg in enumerate(self.ais):
				seg.na12.gbar = na12_map[i]
				seg.na16.gbar = na16_map[i]
				seg.kvDF.gbar = aik
		
		elif na_type == 7:
			self.ais.insert('na12')
			self.ais.insert('na16')
			self.ais.insert('kvDF')
			num = self.ais.nseg
			na12_map = np.hstack((np.array([aina12*0.3]*int(num*0.2)), 
						 np.array([aina12]*int(num*0.3)),
						 np.array([aina12*0.3]*int(num*0.5))))
			na16_map = np.hstack((np.array([aina16*0.3]*int(num*0.5)),
						 np.array([aina16]*int(num*0.3)),
						 np.array([aina16*0.3]*int(num*0.2))))
			for i,seg in enumerate(self.ais):
				seg.na12.gbar = na12_map[i]
				seg.na16.gbar = na16_map[i]
				seg.kvDF.gbar = aik
				
		elif na_type == 8:
			self.ais.insert('na12')
			self.ais.insert('na16')
			self.ais.insert('kvDF')
			num = self.ais.nseg
			na12_map = np.linspace(aina12,aina12,num)
			na16_map = np.linspace(aina16,aina16,num)
			for i,seg in enumerate(self.ais):
				seg.na12.gbar = na12_map[i]
				seg.na16.gbar = na16_map[i]
				seg.kvDF.gbar = aik
		
		elif na_type == 9:
			self.ais.insert('na12')
			self.ais.insert('na16')
			self.ais.insert('kvDF')
			num = self.ais.nseg
			dens = [0.6,0.9,1,0.9,0.6,0.5,0.4,0.3,0.2,0.1]
			na12_map = []
			na16_map = []
			for i in range(10):
				for j in range(int(num*0.1)):
					na12_map.append(dens[i] * aina12)
					na16_map.insert(0, dens[i] * aina16)
			for i,seg in enumerate(self.ais):
				seg.na12.gbar = na12_map[i]
				seg.na16.gbar = na16_map[i]
				seg.kvDF.gbar = aik

def attach_current_clamp(cell, loc=0.5, delay=3, dur=1, amp=.6):
	# Attach a current clamp to a neuron
	#   :param cell: Cell object to attach the current clamp.
    #	:param loc: Location on the soma where the stimulus is placed.
	#	:param delay: Onset of the injected current.
    #	:param dur: Duration of the stimulus.
    #	:param amp: Magnitude of the current.
    
    stim = h.IClamp(cell.soma(loc))
    stim.delay = delay
    stim.dur = dur
    stim.amp = amp
    return stim


def set_recording_vectors(cell):
	# Set soma, dendrite, and time recording vectors on the cell.
    #	:param cell: Cell to record from.
    #	:return: the soma, dendrite, and time vectors as a tuple.
	vec = {}    # A dictionary to save voltage of all sections
	nseg = []
	secset = []
	nseg = [1, 20, cell.soma.nseg, cell.hill.nseg, cell.ais.nseg, 50]
	secset = ['t', 'v_dend1', 'v_soma', 'v_hill', 'v_ais', 'v_axon']
	for v, var in enumerate(secset):
#    	print(var)
		for n in range(nseg[v]):
			vec_name = var+'_'+str(n)
			vec[vec_name] = h.Vector()
			if var == 'v_dend1':
				vec[vec_name].record(cell.dend1((2*(cell.dend1.nseg-nseg[v]+n+1)-1)/(cell.dend1.nseg*2))._ref_v)
			elif var == 'v_soma':
				vec[vec_name].record(cell.soma((2*(n+1)-1)/(cell.soma.nseg*2))._ref_v)
			elif var == 'v_hill':
				vec[vec_name].record(cell.hill((2*(n+1)-1)/(cell.hill.nseg*2))._ref_v)
			elif var == 'v_ais':
				vec[vec_name].record(cell.ais((2*(n+1)-1)/(cell.ais.nseg*2))._ref_v)
			elif var == 'v_axon':
				vec[vec_name].record(cell.axon((2*(n+1)-1)/(cell.axon.nseg*2))._ref_v)
			else:
				vec[vec_name].record(h._ref_t)
	return vec


def simulate(celsius=20, tstop=20, dt=0.001):
    #Initialize and run a simulation.
	#	:param tstop: Duration of the simulation.	
	#	:param dt: time resolution (ms).	
    h.celsius = celsius
    h.tstop = tstop
    h.dt = dt    
    h.run()


def show_output(vec, path):
	# Draw the output.
	#	:param vec: Membrane potential vector of all segments.
	#   :param path: Path where to save the potentials
	
	
	plt.figure()
	for index, k in enumerate(vec.keys()):
		if index == 0:
			continue
		plt.plot(vec[k])
	plt.xlabel('time (ms)')
	plt.ylabel('mV')
	plt.show()
	if path:
		plt.savefig(path + 'ap.png')
		plt.close()
    
	
	seg_dend1 = []
	seg_soma = []
	seg_hill = []
	seg_ais = []
	seg_axon = []
	peakt_dend1 = []
	peakt_soma = []
	peakt_hill = []
	peakt_ais = []
	peakt_axon = []
	flag = 0
	for i, k in enumerate(vec.keys()):
		if 'dend1' in k:
			seg_dend1.append(i)
			peakt_dend1.append(np.argmax(vec[k]))
		elif 'soma' in k:
			seg_soma.append(i)
			peakt_soma.append(np.argmax(vec[k]))
		elif 'hill' in k:
			flag = 1
			seg_hill.append(i)
			peakt_hill.append(np.argmax(vec[k]))
		elif 'ais' in k:
			seg_ais.append(i)
			peakt_ais.append(np.argmax(vec[k]))
		elif 'axon' in k:
			seg_axon.append(i)
			peakt_axon.append(np.argmax(vec[k]))
	plt.figure()
	plt.plot(seg_dend1, peakt_dend1, label='dend1', marker='o')
	plt.plot(seg_soma, peakt_soma, label='soma', marker='o')
	if flag == 1:
		plt.plot(seg_hill, peakt_hill, label='hill', marker='o')
	plt.plot(seg_ais, peakt_ais, label='ais', marker='o')
	plt.plot(seg_axon, peakt_axon, label='axon', marker='o')
	plt.legend()
	plt.show()
	if path:
		plt.savefig(path+'peakt.png')
		plt.close()


def save_vec(vec, path):
    name = path + 'v_vec.p'
    file = open(name, 'w')
    file.close()
    with open(name, 'ab') as file:
        pickle.dump(vec, file)


def cal_velocity(vec, seg):
	h.dt = 0.001
	# calculate the velocity of the seg
    #	:param vec: Membrane potential vector of all segments.
	#   :param seg: Segment where to calculate the velocity
	#   :output: Velocity of the segment

	# find peak time
	peakt_ais = []
	peakt_axon = []
	for k in vec.keys():
		t = k.split('_')[1]
		if t in seg:
			if t == 'ais':
				pt = np.argmax(vec[k])
				peakt_ais.append(pt)		
			elif t == 'axon':
				pt = np.argmax(vec[k])
				peakt_axon.append(pt)
	
	# calculate the velocity	
	aisbp_velocity = 0
	aisfw_velocity = 0
	axon_velocity = 0
	if 'ais' in seg:
		initial_point = np.argmin(peakt_ais)
#		plt.figure()
#		for i in range(initial_point):
#			plt.plot(vec['v_ais_'+str(i)],color=[1-0.024*i,0,0.024*i], label='v_ais_'+str(i))		
		ds = float(len(peakt_ais[0:initial_point])-1)
		dt = float(peakt_ais[0] - peakt_ais[initial_point])
		aisbp_velocity = 0 if dt == float(0) else ds / dt / h.dt
		ds = float(len(peakt_ais[initial_point:])-1)
		dt = float(peakt_ais[-1] - peakt_ais[initial_point])
		aisfw_velocity = 0 if dt == float(0) else ds / dt / h.dt
	if 'axon' in seg:
		ds = float(len(peakt_axon)-1)
		dt = float(peakt_axon[-1] - peakt_axon[0])
		axon_velocity = 0 if dt == float(0) else ds / dt / h.dt

	return aisbp_velocity, aisfw_velocity, axon_velocity


def cal_relative_initial_point(vec):
	# find peak time
	peakt = []
	for k in vec.keys():
		if 'ais' in k:
			pt = np.argmax(vec[k])
			peakt.append(pt)
	index = np.argmin(peakt)
	relative_initial_point = float(index) / float(len(peakt))
	return index, relative_initial_point


def load_data(file_path):
	bpv_len = None
	fwv_len = None
	bpv_dist = None
	fwv_dist = None
	with open(file_path+'bpv_len.p', 'rb') as file:
		bpv_len = pickle.load(file)
	with open(file_path+'fwv_len.p', 'rb') as file:
		fwv_len = pickle.load(file)
	with open(file_path+'bpv_dist.p', 'rb') as file:
		bpv_dist = pickle.load(file)
	with open(file_path+'fwv_dist.p', 'rb') as file:
		fwv_dist = pickle.load(file)
	return bpv_len, fwv_len, bpv_dist, fwv_dist


def load_data_3d(file_path):
	bpv = None
	fwv = None
	with open(file_path+'bpv.p', 'rb') as file:
		bpv = pickle.load(file)
	with open(file_path+'fwv.p', 'rb') as file:
		fwv = pickle.load(file)
	return bpv, fwv


def show_data(bpv_len, fwv_len, bpv_dist, fwv_dist, legt, leg):
	plt.figure(figsize=(8,4.5))
	
	plt.subplot(2,2,1)	
	x = np.linspace(10,70,7)
	l = len(bpv_len)
	for i,v in enumerate(bpv_len):
		index = np.nonzero(v)
		plt.plot(x[index], v[index], color = [i/l,0,1-i/l], label=legt+'='+str(int(leg[i])), marker='s')
	plt.xlabel('AIS length (' + r'$\mu$' + 'm)')
	plt.ylabel('AIS bpAP velocity (' + r'$\mu$' + 'm/ms)')
	plt.xticks(x)
	
	plt.subplot(2,2,2)
	l = len(fwv_len)
	for i,v in enumerate(fwv_len):
		index = np.nonzero(v)
		plt.plot(x[index], v[index], color = [i/l,0,1-i/l], label=legt+'='+str(int(leg[i])), marker='s')
	plt.xlabel('AIS length (' + r'$\mu$' + 'm)')
	plt.ylabel('AIS fwAP velocity (' + r'$\mu$' + 'm/ms)')
	plt.xticks(x)
	plt.legend(loc='center right', bbox_to_anchor=(1.7, 0.42))
	
	plt.subplot(2,2,3)
	x = np.linspace(3,33,7)
	l = len(bpv_dist)
	for i,v in enumerate(bpv_dist):
		index = np.nonzero(v)
		plt.plot(x[index], v[index], color = [i/l,0,1-i/l], label=legt+'='+str(int(leg[i])), marker='s')
	plt.xlabel('AIS distance (' + r'$\mu$' + 'm)')
	plt.ylabel('AIS bpAP velocity (' + r'$\mu$' + 'm/ms)')
	plt.xticks(x)
	
	plt.subplot(2,2,4)
	l = len(fwv_dist)
	for i,v in enumerate(fwv_dist):
		index = np.nonzero(v)
		plt.plot(x[index], v[index], color = [i/l,0,1-i/l], label=legt+'='+str(int(leg[i])), marker='s')
	plt.xlabel('AIS distance (' + r'$\mu$' + 'm)')
	plt.ylabel('AIS fwAP velocity (' + r'$\mu$' + 'm/ms)')
	plt.xticks(x)	
	plt.tight_layout()



def show_data_fit(bpv_len, fwv_len, bpv_dist, fwv_dist, title):
	plt.figure(figsize=(8,6))
	
	plt.subplot(2,2,1)	
	x = np.linspace(10,70,7)
	l = len(bpv_len)
	for i,v in enumerate(bpv_len):
		index = np.nonzero(v)
		plt.plot(x[index], v[index], color = [i/l,0,1-i/l], marker='s')
	plt.xlabel('AIS length (' + r'$\mu$' + 'm)')
	plt.ylabel('AIS bpAP velocity (' + r'$\mu$' + 'm/ms)')
	plt.xticks(x)
	plt.title(title)
	
	plt.subplot(2,2,2)
	l = len(fwv_len)
	for i,v in enumerate(fwv_len):
		index = np.nonzero(v)
		plt.plot(x[index], v[index], color = [i/l,0,1-i/l], marker='s')
	plt.xlabel('AIS length (' + r'$\mu$' + 'm)')
	plt.ylabel('AIS fwAP velocity (' + r'$\mu$' + 'm/ms)')
	plt.xticks(x)
	
	plt.subplot(2,2,3)
	x = np.linspace(3,33,7)
	l = len(bpv_dist)
	for i,v in enumerate(bpv_dist):
		index = np.nonzero(v)
		plt.plot(x[index], v[index], color = [i/l,0,1-i/l], marker='s')
	plt.xlabel('AIS distance (' + r'$\mu$' + 'm)')
	plt.ylabel('AIS bpAP velocity (' + r'$\mu$' + 'm/ms)')
	plt.xticks(x)
	
	plt.subplot(2,2,4)
	l = len(fwv_dist)
	for i,v in enumerate(fwv_dist):
		index = np.nonzero(v)
		plt.plot(x[index], v[index], color = [i/l,0,1-i/l], marker='s')
	plt.xlabel('AIS distance (' + r'$\mu$' + 'm)')
	plt.ylabel('AIS fwAP velocity (' + r'$\mu$' + 'm/ms)')
	plt.xticks(x)
	plt.tight_layout()
