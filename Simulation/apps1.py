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


# function: Cdv/dt = icap = -(ina+ik+ileak+iax)


#cell = nm.NeuronModel(dl=1000, dd=2,  sl=40, sd=20, \
#				   hl=10, hd=2, ail=40, aid=1.2, axl=1000, axd=1.2,\
#				   dna=100, sna=100, hna=300, aina=4000, axna=300, dk=20, \
#				   sk=20, hk=150, aik=1000, axk=150,\
#				   na_type=8, aina12=3000, aina16=3000)
#stim = nm.attach_current_clamp(cell, amp=1, dur=1)
#vec = nm.set_recording_vectors(cell)
#

#vs = h.Vector()
#vs.record(cell.ais(locs)._ref_v)
#inas = h.Vector()
#inas.record(cell.ais(locs)._ref_ina)
#iks = h.Vector()
#iks.record(cell.ais(locs)._ref_ik)
#
#vi = h.Vector()
#vi.record(cell.ais(loci)._ref_v)
#inai = h.Vector()
#inai.record(cell.ais(loci)._ref_ina)
#iki = h.Vector()
#iki.record(cell.ais(loci)._ref_ik)
#
#ve = h.Vector()
#ve.record(cell.ais(loce)._ref_v)
#inae = h.Vector()
#inae.record(cell.ais(loce)._ref_ina)
#ike = h.Vector()
#ike.record(cell.ais(loce)._ref_ik)
#
#
#
#nm.simulate()
#nm.show_output(vec, None)
#bpv, fwv, __ = nm.cal_velocity(vec, seg)
#index1, __ = nm.cal_relative_initial_point(vec)
#
#difvs = np.append(np.diff(vs)/1000/h.dt,0)
#iaxials = difvs + inas + iks
#difvi = np.append(np.diff(vi)/1000/h.dt,0)
#iaxiali = difvi + inai + iki
#difve = np.append(np.diff(ve)/1000/h.dt,0)
#iaxiale = difve + inae + ike
#
#z = np.array([0]*len(inas))
#
#plt.figure()
#plt.plot(z-inas,color='r')
#plt.plot(z-iks,color='r',linestyle=':')
#plt.plot(iaxials,color='r',linestyle='--')
#plt.plot(z-inai,color='g')
#plt.plot(z-iki,color='g',linestyle=':')
#plt.plot(iaxiali,color='g',linestyle='--')
#plt.plot(z-inae,color='b')
#plt.plot(z-ike,color='b',linestyle=':')
#plt.plot(iaxiale,color='b',linestyle='--')
#plt.grid()
#plt.title('Na: 8000')
#plt.xticks(np.linspace(0,20000+1,201))
#plt.ylim((-6,6))
#
#plt.figure()
#plt.plot(vs, color='r')
#plt.plot(vi, color='g')
#plt.plot(ve, color='b')
#plt.grid()
#plt.xticks(np.linspace(0,20000+1,201))
#plt.ylim((-80,40))
#
#
#
#print('normal:',bpv,fwv)
#cell.dend1 = None
#cell.soma = None
#cell.hill = None
#cell.ais  = None
#cell.axon = None
#for sec in h.allsec():
#	print(sec)
#	
#	
##############################################################################


#plt.close('all')

def current(loci, ail):
	cell = nm.NeuronModel(dl=1000, dd=2,  sl=40, sd=20,\
					   hl=10, hd=2, ail=ail, aid=1.2, axl=1000, axd=1.2,\
					   dna=100, sna=100, hna=300, aina=4000, axna=300, dk=20,\
					   sk=20, hk=150, aik=1000, axk=150,\
					   na_type=7, aina12=1000, aina16=1000)
	stim = nm.attach_current_clamp(cell, amp=1, dur=1)
	vec = nm.set_recording_vectors(cell)
	v = h.Vector()
	v.record(cell.ais(loci)._ref_v)
	
	icap = h.Vector() # (mA/cm2)
	icap.record(cell.ais(loci)._ref_i_cap)
	
	ileak = h.Vector() # (mA/cm2)
	ileak.record(cell.ais(loci)._ref_i_pas)
	
	ina = h.Vector() # (mA/cm2)
	ina.record(cell.ais(loci)._ref_ina)
	
	ik = h.Vector() # (mA/cm2)
	ik.record(cell.ais(loci)._ref_ik)
	
	nm.simulate()
	print(nm.cal_velocity(vec, ["ais"]))
	
	iax = -np.array(icap.to_python()) - np.array(ileak.to_python()) - np.array(ina.to_python()) - np.array(ik.to_python())
	
	cell.dend1 = None
	cell.soma = None
	cell.hill = None
	cell.ais  = None
	cell.axon = None
	for sec in h.allsec():
		print(sec)
	return v, icap, ileak, ina, ik, iax


#ail = 40
#loci1 = 22.5/40
#loci2 = 0.5/40
#loci3 = 39.5/40
ail = 60
loci1 = 31.5/60
loci2 = 9.5/60
loci3 = 48.5/60
v1, icap1, ileak1, ina1, ik1, iax1 = current(loci1, ail)
v2, icap2, ileak2, ina2, ik2, iax2 = current(loci2, ail)
v3, icap3, ileak3, ina3, ik3, iax3 = current(loci3, ail)
ds = 0.025
plt.figure()
plt.subplot(231)
plt.plot(v1)
plt.plot(v2)
plt.plot(v3)
plt.ylim(-80,40)
plt.title("voltage")
plt.ylabel("mV")
plt.subplot(232)
plt.plot(icap1)
plt.plot(icap2)
plt.plot(icap3)
plt.ylim(-0.025,0.125)
plt.title("capacity current")
plt.ylabel("mA/cm2")
plt.subplot(233)
plt.plot(ileak1)
plt.plot(ileak2)
plt.plot(ileak3)
plt.ylim(-0.002,0.011)
plt.title("leaky current")
plt.ylabel("mA/cm2")
plt.subplot(234)
plt.plot(ina1)
plt.plot(ina2)
plt.plot(ina3)
plt.ylim(-0.7,0.05)
plt.title("na current")
plt.ylabel("mA/cm2")
plt.subplot(235)
plt.plot(ik1)
plt.plot(ik2)
plt.plot(ik3)
plt.ylim(-0.05,1.2)
plt.title("k current")
plt.ylabel("mA/cm2")
plt.subplot(236)
plt.plot(iax1)
plt.plot(iax2)
plt.plot(iax3)
plt.ylim(-1.1,0.6)
plt.title("iaxial")
plt.ylabel("mA/cm2")


#vs = h.Vector()
#vs.record(cell.ais(locs)._ref_v)
#inas = h.Vector()
#inas.record(cell.ais(locs)._ref_ina)
#iks = h.Vector()
#iks.record(cell.ais(locs)._ref_ik)
#
#vil = h.Vector()
#vil.record(cell.ais(loci-ds)._ref_v)
#vi = h.Vector()
#vi.record(cell.ais(loci)._ref_v)
#vir = h.Vector()
#vir.record(cell.ais(loci+ds)._ref_v)
#inai = h.Vector()
#inai.record(cell.ais(loci)._ref_ina)
#iki = h.Vector()
#iki.record(cell.ais(loci)._ref_ik)
#icap = h.Vector()
#icap.record(cell.ais(loci)._ref_i_cap)
#
#ve = h.Vector()
#ve.record(cell.ais(loce)._ref_v)
#inae = h.Vector()
#inae.record(cell.ais(loce)._ref_ina)
#ike = h.Vector()
#ike.record(cell.ais(loce)._ref_ik)
#
#
#nm.simulate()
#nm.show_output(vec, None)
#bpv, fwv, __ = nm.cal_velocity(vec, seg)
#index2, __ = nm.cal_relative_initial_point(vec)
#
#difvs = np.append(np.diff(vs)/1000/h.dt,0)
#iaxials = difvs + inas + iks
#difvi = np.append(np.diff(vi)/1000/h.dt,0)
#ili = (np.array(vi.to_python())+65)*1.2*np.pi*(10**(-12))
#
#iaxiali = difvi + inai + iki + ili
#iaxialil = (np.array(vil.to_python()) - np.array(vi.to_python())) / r
#iaxialir = (np.array(vir.to_python()) - np.array(vi.to_python())) / r
#difve = np.append(np.diff(ve)/1000/h.dt,0)
#iaxiale = difve + inae + ike
#
#plt.figure()
#plt.plot(icap)
#plt.plot(difvi)
#plt.show()
#
#plt.figure()
#ax = plt.subplot(111)
#ax.plot(iaxialil, label='left')
#ax.plot(iaxialir, label='right')
#ax.plot(iaxialil + iaxialir, label='sum')
#ax.plot(iaxiali, label='minus')
#ax.plot(ili, label='leak')
#ax.legend()
#plt.show()
#
#plt.figure()
#plt.plot(z-inas,color='r')
#plt.plot(z-iks,color='r',linestyle=':')
#plt.plot(iaxials,color='r',linestyle='--')
#plt.plot(z-inai,color='g')
#plt.plot(z-iki,color='g',linestyle=':')
#plt.plot(iaxiali,color='g',linestyle='--')
#plt.plot(z-inae,color='b')
#plt.plot(z-ike,color='b',linestyle=':')
#plt.plot(iaxiale,color='b',linestyle='--')
#plt.grid() 
#plt.title('Na: 1000')
#plt.xticks(np.linspace(0,20000+1,201))
#plt.ylim((-6,6))
#
#plt.figure()
#plt.plot(vs, color='r')
#plt.plot(vi, color='g')
#plt.plot(ve, color='b')
#plt.grid()
#plt.xticks(np.linspace(0,20000+1,201))
#plt.ylim((-80,40))


#print('apps1:',bpv,fwv)


#cell.dend1 = None
#cell.soma = None
#cell.hill = None
#cell.ais  = None
#cell.axon = None
#for sec in h.allsec():
#	print(sec)

