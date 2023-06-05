# Jingcheng Shi
# 06/05/23

from neuron import h, gui
from neuron.units import ms, mV

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

class Cell:
    def __init__(self, gid):
        self._gid = gid
        self._setup_morphology()
        # self.all = self.soma.wholetree()
        # self._setup_biophysics()

        # self.x = self.y = self.z = 0                     # <-- NEW
        # h.define_shape()
        # self._rotate_z(theta)                            # <-- NEW        
        # self._set_position(x, y, z)                      # <-- NEW

    def __repr__(self):
        return '{}[{}]'.format(self.name, self._gid)
    
    # def _set_position(self, x, y, z):
    #     for sec in self.all:
    #         for i in range(sec.n3d()):
    #             sec.pt3dchange(i,
    #                            x - self.x + sec.x3d(i),
    #                            y - self.y + sec.y3d(i),
    #                            z - self.z + sec.z3d(i),
    #                           sec.diam3d(i))
    #     self.x, self.y, self.z = x, y, z
    # def _rotate_z(self, theta):
    #     """Rotate the cell about the Z axis."""
    #     for sec in self.all:
    #         for i in range(sec.n3d()):
    #             x = sec.x3d(i)
    #             y = sec.y3d(i)
    #             c = h.cos(theta)
    #             s = h.sin(theta)
    #             xprime = x * c - y * s
    #             yprime = x * s + y * c
    #             sec.pt3dchange(i, xprime, yprime, sec.z3d(i), sec.diam3d(i))
    

class L5Model(Cell):
    name = 'L5Model'

    # def __init__(self):
    #     self.create_morphology()
    #     # self.insert_channels(variables)
    #     # self.esyn = []
    #     # self.isyn = []
    #     # self.spines = []
    #     # self.num_spines_on_dends = np.zeros(len(self.dendlist))
        
    def _setup_morphology(self):    
        cell = h.Import3d_SWC_read()
        cell.input(morphology)
        i3d = h.Import3d_GUI(cell, 1)
        i3d.instantiate(None)
        # h.define_shape()
        # self.create_sectionlists()
        # self.set_nsegs()

# def create_n_L5Model(n, r):
#     """n = number of cells; r = radius of circle"""
#     cells = []
#     for i in range(n):
#         # theta = i * 2 * h.PI / n
#         cells.append(L5Model(i))
#     return cells  

# Test the code
# my_cells = create_n_L5Model(1, 50)

my_cell = L5Model(0)
h.PlotShape(True).plot(plt)
# ps = h.PlotShape(True)
# ps.show(0)

