from neuron import h
h.load_file("stdlib.hoc")
h.load_file("import3d.hoc")

class Pyramidal:
    def __init__(self):
        self.load_morphology()
        # do discretization, ion channels, etc
    def load_morphology(self):
        cell = h.Import3d_SWC_read()
        cell.input("cell1.swc")
        i3d = h.Import3d_GUI(cell, False)
        i3d.instantiate(self)

pyr = Pyramidal()
a = pyr.all
print('end')
