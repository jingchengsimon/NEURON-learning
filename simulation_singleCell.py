# Jingcheng Shi
# 05/24/23

from neuron import h, gui
from neuron.units import ms, mV
import matplotlib.pyplot as plt
from ballstickModel import create_n_BallAndStick

h.load_file('stdrun.hoc')

my_cells = create_n_BallAndStick(7, 50)
# source
stim = h.NetStim() # Make a new stimulator
stim.number = 1
stim.start = 9

# Attach it to a synapse in the middle of the dendrite
# of the first cell in the network. (Named 'syn_' to avoid
# being overwritten with the 'syn' var assigned later.)
# target
syn_ = h.ExpSyn(my_cells[0].dend(0.5))

# Event-based communication
ncstim = h.NetCon(stim, syn_)
ncstim.delay = 1 * ms
ncstim.weight[0] = 0.04 # NetCon weight is a vector.

syn_.tau = 2 * ms
print('Reversal potential = {} mV'.format(syn_.e))

## Simulation and recording
recording_cell = my_cells[0]
soma_v = h.Vector().record(recording_cell.soma(0.5)._ref_v)
dend_v = h.Vector().record(recording_cell.dend(0.5)._ref_v)
t = h.Vector().record(h._ref_t)

h.finitialize(-65 * mV)
h.continuerun(25 * ms)

syn_i = h.Vector().record(syn_._ref_i)

fig = plt.figure(figsize=(8,4))
ax1 = fig.add_subplot(2, 1, 1)
soma_plot = ax1.plot(t, soma_v, color='black', label='soma(0.5)')
dend_plot = ax1.plot(t, dend_v, color='red', label='dend(0.5)')
rev_plot = ax1.plot([t[0], t[-1]], [syn_.e, syn_.e], label='syn reversal',
        color='blue', linestyle=':')
ax1.legend()
ax1.set_ylabel('mV')
ax1.set_xticks([]) # Use ax2's tick labels

# ax2 = fig.add_subplot(2, 1, 2)
# syn_plot = ax2.plot(t, syn_i, color='blue', label='synaptic current')
# ax2.legend()
# ax2.set_ylabel(h.units('ExpSyn.i'))
# ax2.set_xlabel('time (ms)')

plt.show()
