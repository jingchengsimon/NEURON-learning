# Jingcheng Shi
# 06/05/23

from neuron import h, gui
from neuron.units import ms, mV

import plotly.graph_objects as go
import matplotlib.pyplot as plt

import os
import numpy as np
import pandas as pd

from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection

h.load_file('stdrun.hoc')
h.load_file('import3d.hoc')

swc_file = 'cell1'
morphology = "./{x}.swc".format(x=swc_file)

## edit .swc file, average x, y, z of all rows which type equals 17(column 2) 
# and set a new row which type equals 1

def alter_swc(file,old_str,new_str):
    file_data = ""
    with open(file,'r') as f:
        for line in f:
            if line.startswith("#"):
                continue
            line_s = line.split()
            if line_s[1] == old_str:
                line = line.replace(old_str,new_str)
            file_data += line
    with open(file, "w") as f:
        f.write(file_data)
 
alter_swc(morphology, "17", "1")

# segs = pd.read_csv(morphology,comment='#',sep=' ',
#     names=['id','type','x','y','z','r','pid'])
# segs_soma = segs[segs['type'] == 17]
# # fig = plt.figure()
# # plt.scatter(segs_soma['x'],segs_soma['y'])

# avg_x = round(segs_soma['x'].mean(),2)
# avg_y = round(segs_soma['y'].mean(),2)
# avg_z = round(segs_soma['z'].mean(),2)
# avg_r = round(segs_soma['r'].mean(),2)
# # segs = segs.append({'id':segs['id'].max()+1,'type':1,
#     # 'x':avg_x,'y':avg_y,'z':avg_z,'r':0,'pid':-1},ignore_index=True)

# with open(morphology, 'a+') as f:
#     f.write('\n{id} {type} {x} {y} {z} {r} {pid}'.format(
#         id=segs['id'].max()+1,type=1,x=avg_x,y=avg_y,z=avg_z,r=avg_r,pid=-1))

class Cell:
    def __init__(self, gid):
        self._gid = gid
        self._setup_morphology()
        self._setup_biophysics()
        #self._setup_mod()
        
    def __repr__(self):
        return '{}[{}]'.format(self.name, self._gid)
    
class L5Model(Cell):
    name = 'L5Model'

    def _setup_morphology(self):    
        cell = h.Import3d_SWC_read()
        cell.input(morphology)
        i3d = h.Import3d_GUI(cell, False)
        i3d.instantiate(self)

    def _setup_biophysics(self):
        for sec in self.all:
            sec.insert('pas')  
            sec.Ra = 100    # Axial resistance in Ohm * cm
            if ('soma' in sec.hname()) or ('axon' in sec.hname()):
                sec.cm = 1
            else:
                sec.cm = 2
            for seg in sec:
                # seg.pas.g = 0.001  # Passive conductance in S/cm2
                seg.pas.e = -90   # Leak reversal potential mV
            # print('L5Model' in sec.hname())
            # print('L5Model' in str(sec))
            # print(sec.psection())
            # print("type(sec) = {}".format(type(sec)))
    
    # def _setup_mod(self):
            

my_cell = L5Model(0)
h.topology()
s = h.Shape()

## Visualize
h.PlotShape(True).plot(plt)
# ps = h.PlotShape(True)
# ps.show(0)

## Simulate
soma = my_cell.soma[0]
print(soma.psection())

ic = h.IClamp(soma(0.5))
ic.amp = 10
ic.dur = 1
ic.delay = 5
print(soma.psection())

v = h.Vector().record(soma(0.5)._ref_v)             # Membrane potential vector
t = h.Vector().record(h._ref_t)                     # Time stamp vector
amp = h.Vector().record(ic._ref_i)

h.finitialize(-90 * mV)
h.continuerun(30 * ms)

## Visualize
plt.figure()
plt.plot(t, v)
plt.xlabel('t (ms)')
plt.ylabel('v (mV)')
plt.show()
plt.savefig('Injection.jpg')
# from bokeh.io import output_notebook
# import bokeh.plotting as plt
# output_notebook()

