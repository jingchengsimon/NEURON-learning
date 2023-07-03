from neuron import h
h.load_file('stdrun.hoc')
h.nrn_load_dll('./arm64/.libs/libnrnmech.so') # load modfiles

h.load_file(cell_folder+'L5PCbiophys3.hoc') # load biophysics

h.load_file("import3d.hoc") # load morphology

h.load_file(cell_folder+'L5PCtemplate.hoc') # load builder
complex_cell = h.L5PCtemplate(cell_folder+'cell1.asc') # build complex_cell object