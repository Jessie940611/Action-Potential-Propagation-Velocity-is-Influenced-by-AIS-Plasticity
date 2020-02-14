# -*- coding: utf-8 -*-
"""
Created on Mon Oct  7 16:34:40 2019

somatic data vs. dendritic data

@author: cbi
"""

import neuronmodel as nm
import numpy as np
from matplotlib import pyplot as plt 
from neuron import h
import os
import pickle


plt.close('all')
seg = ['ais']

cell = nm.NeuronModel(dl=1000, dd=2,  sl=40, sd=20, \
				   hl=10, hd=2, ail=40, aid=1.2, axl=1000, axd=1.2,\
				   dna=100, sna=100, hna=300, aina=4000, axna=300, dk=20, \
				   sk=20, hk=150, aik=1000, axk=150,\
				   na_type=6, aina12=6000, aina16=6000)
stim = nm.attach_current_clamp(cell, amp=1.0)
vec = nm.set_recording_vectors(cell)
nm.simulate()
nm.show_output(vec, None)
bpv, fwv, __ = nm.cal_velocity(vec, seg)
print('normal:',bpv,fwv)
cell.dend1 = None
cell.soma = None
cell.hill = None
cell.ais  = None
cell.axon = None
for sec in h.allsec():
	print(sec)


cell = nm.NeuronModel(dl=1000, dd=2,  sl=40, sd=20,\
				   hl=10, hd=2, ail=60, aid=1.2, axl=1000, axd=1.2,\
				   dna=100, sna=100, hna=300, aina=4000, axna=300, dk=20,\
				   sk=20, hk=150, aik=500, axk=150,\
				   na_type=8, aina12=1800, aina16=1800)
stim = nm.attach_current_clamp(cell, amp=1.0)
vec = nm.set_recording_vectors(cell)
nm.simulate()
nm.show_output(vec, None)
bpv, fwv, __ = nm.cal_velocity(vec, seg)
print('apps1:',bpv,fwv)
cell.dend1 = None
cell.soma = None
cell.hill = None
cell.ais  = None
cell.axon = None
for sec in h.allsec():
	print(sec)

