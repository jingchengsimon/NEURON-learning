# Jingcheng Shi
# 05/25/23
from neuron import h, gui
from neuron.units import ms, mV
import matplotlib.pyplot as plt
from ballstickModel import create_n_BallAndStick

h.load_file('stdrun.hoc')

my_cells = create_n_BallAndStick(7, 50)

## Start stimulation
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

## Construct the network connection
syns = []
netcons = []
# source and target
for source, target in zip(my_cells, my_cells[1:] + [my_cells[0]]):
    syn = h.ExpSyn(target.dend(0.5))
    nc = h.NetCon(source.soma(0.5)._ref_v, syn, sec=source.soma)
    nc.weight[0] = 0.05
    nc.delay = 5
    netcons.append(nc)
    syns.append(syn)

# Simulation and recording
recording_cell_0 = my_cells[0]
soma_v_0 = h.Vector().record(recording_cell_0.soma(0.5)._ref_v)
dend_v_0 = h.Vector().record(recording_cell_0.dend(0.5)._ref_v)
t = h.Vector().record(h._ref_t)

recording_cell_1 = my_cells[5]
soma_v_1 = h.Vector().record(recording_cell_1.soma(0.5)._ref_v)
dend_v_1 = h.Vector().record(recording_cell_1.dend(0.5)._ref_v)

spike_times = [h.Vector() for nc in netcons]
for nc, spike_times_vec in zip(netcons, spike_times):
    nc.record(spike_times_vec)

h.finitialize(-65 * mV)
h.continuerun(100 * ms)

fig = plt.figure(figsize=(8,4))
ax1 = fig.add_subplot(2, 1, 1)
plt.plot(t, soma_v_0, label='soma(0.5)')
plt.plot(t, dend_v_0, label='dend(0.5)')
plt.title('Cell 0')
plt.legend()

ax1 = fig.add_subplot(2, 1, 2)
plt.plot(t, soma_v_1, label='soma(0.5)')
plt.plot(t, dend_v_1, label='dend(0.5)')
plt.legend()
plt.title('Cell 1')

# plt.show()

plt.figure()
for i, spike_times_vec in enumerate(spike_times):
    print('cell {}: {}'.format(i, list(spike_times_vec)))
    plt.vlines(spike_times_vec, 1, 7, linestyles='dashed', colors='red', alpha=0.5)
    plt.vlines(spike_times_vec, i + 0.5, i + 1.5)
    
plt.show()