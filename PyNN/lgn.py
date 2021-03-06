from pyNN.utility import get_script_args, Timer
import numpy as np
import matplotlib.pyplot as plt 
import pyNN.space as space
from connector_functions import gabor_probability, lgn_to_cortical_connection, create_lgn_to_cortical
from connector_functions import create_cortical_to_cortical_connection, create_thalamocortical_connection
import cPickle

#############################

#simulator_name = get_script_args(1)[0]
#exec("import pyNN.%s as simulator" % simulator_name)

#simulator_name = 'nest'
#exec("import pyNN.%s as simulator" % simulator_name)

import pyNN.nest as simulator


#############################
# Load LGN spikes and positions
#############################
directory = './data/'
format = '.cpickle'

## Load space 
layer = '_layer' + str(0)

polarity = '_on'
mark = 'positions'
positions_filename = directory + mark + polarity + layer + format
f1 = open(positions_filename, "rb")
positions_on = cPickle.load(f1)
f1.close()

polarity = '_off'
mark = 'positions'
positions_filename = directory + mark + polarity + layer + format
f1 = open(positions_filename, "rb")
positions_off = cPickle.load(f1)
f1.close()

## Load the spikes 

#  Layer 1  
layer = '_layer' + str(0)

polarity = '_on'
mark = 'spike_train'
spikes_filename = directory + mark + polarity + layer + format
f2 = open(spikes_filename, 'rb')
spikes_on_0 = cPickle.load(f2)
f2.close()

polarity = '_off'
mark = 'spike_train'
spikes_filename = directory + mark + polarity + layer + format
f2 = open(spikes_filename, 'rb')
spikes_off_0 = cPickle.load(f2)
f2.close()

#  Layer 0
layer = '_layer' + str(1)

polarity = '_on'
mark = 'spike_train'
spikes_filename = directory + mark + polarity + layer + format
f2 = open(spikes_filename, 'rb')
spikes_on_1 = cPickle.load(f2)
f2.close()

polarity = '_off'
mark = 'spike_train'
spikes_filename = directory + mark + polarity + layer + format
f2 = open(spikes_filename, 'rb')
spikes_off_1 = cPickle.load(f2)
f2.close()

#  Layer 2  
layer = '_layer' + str(2)

polarity = '_on'
mark = 'spike_train'
spikes_filename = directory + mark + polarity + layer + format
f2 = open(spikes_filename, 'rb')
spikes_on_2 = cPickle.load(f2)
f2.close()

polarity = '_off'
mark = 'spike_train'
spikes_filename = directory + mark + polarity + layer + format
f2 = open(spikes_filename, 'rb')
spikes_off_2 = cPickle.load(f2)
f2.close()

#  Layer 2  
layer = '_layer' + str(3)

polarity = '_on'
mark = 'spike_train'
spikes_filename = directory + mark + polarity + layer + format
f2 = open(spikes_filename, 'rb')
spikes_on_3 = cPickle.load(f2)
f2.close()

polarity = '_off'
mark = 'spike_train'
spikes_filename = directory + mark + polarity + layer + format
f2 = open(spikes_filename, 'rb')
spikes_off_3 = cPickle.load(f2)
f2.close()

#############################
## Network and Simulation parameters
#############################
Ncells_lgn = 30
Ncell_exc = 10
Ncell_inh = 5
#Ncell_exc = 40
#Ncell_inh = 20

t = 1000.0  # Simulation time

# Set the random set for reproducibility
seed = 1055
np.random.seed(seed)

# Has to be called at the beginning of the simulation
simulator.setup(timestep=0.1, min_delay=0.1, max_delay=5.0)

def spike_times_on(i):
    '''
    Test function
    '''

    A = []
    for k in range(len(i)):
        A.append(spikes_on_1[k])

    return A

def spike_times_on_0(i):
    return spikes_on_0

def spike_times_off_0(i):
    return spikes_off_0


def spike_times_on_1(i):
    return spikes_on_1

def spike_times_off_1(i):
    return spikes_off_1

def spike_times_on_2(i):
    return spikes_on_2

def spike_times_off_2(i):
    return spikes_off_2

def spike_times_on_3(i):
    return spikes_on_3

def spike_times_off_3(i):
    return spikes_off_3

# Spatial structure of on LGN cells
# On cells
x0, y0 = positions_on[0] # Take out the lower corner from the positions
x_end, y_end = positions_on[-1]
x1, dummy = positions_on[Ncells_lgn]
dummy, y1 = positions_on[1]
dx = x1 - x0
dy = y1 - y0
lx = x_end - x0
ly = y_end - y0


lgn_structure_on = space.Grid2D(aspect_ratio=1, x0=x0, y0=y0, dx=dx, dy=dy, z=0)

# Off cells
x0, y0 = positions_off[0] # Take out the lower corner from the positions
x_end, y_end = positions_off[-1]
x1, dummy = positions_off[Ncells_lgn]
dummy, y1 = positions_off[1]
dx = x1 - x0
dy = y1 - y0
lx = x_end - x0
ly = y_end - y0

lgn_structure_off = space.Grid2D(aspect_ratio=1, x0=x0, y0=y0, dx=dx, dy=dy, z=0)

# Spikes for LGN populations
lgn_spikes_on_model_0 = simulator.SpikeSourceArray(spike_times=spike_times_on_0)
lgn_spikes_off_model_0 = simulator.SpikeSourceArray(spike_times=spike_times_off_0)

lgn_spikes_on_model_1 = simulator.SpikeSourceArray(spike_times=spike_times_on_1)
lgn_spikes_off_model_1 = simulator.SpikeSourceArray(spike_times=spike_times_off_1)

lgn_spikes_on_model_2 = simulator.SpikeSourceArray(spike_times=spike_times_on_2)
lgn_spikes_off_model_2 = simulator.SpikeSourceArray(spike_times=spike_times_off_2)

lgn_spikes_on_model_3 = simulator.SpikeSourceArray(spike_times=spike_times_on_3)
lgn_spikes_off_model_3 = simulator.SpikeSourceArray(spike_times=spike_times_off_3)

# LGN Popluations
lgn_neurons_on = simulator.Population(Ncells_lgn**2, lgn_spikes_on_model_0, structure=lgn_structure_on, label='LGN_on')
lgn_neurons_off = simulator.Population(Ncells_lgn**2, lgn_spikes_off_model_0, structure=lgn_structure_off, label='LGN_off')

lgn_neurons_on_1 = simulator.Population(Ncells_lgn**2, lgn_spikes_on_model_1, structure=lgn_structure_on, label='LGN_on')
lgn_neurons_off_1 = simulator.Population(Ncells_lgn**2, lgn_spikes_off_model_1, structure=lgn_structure_off, label='LGN_off')

lgn_neurons_on_2 = simulator.Population(Ncells_lgn**2, lgn_spikes_on_model_2, structure=lgn_structure_on, label='LGN_on')
lgn_neurons_off_2 = simulator.Population(Ncells_lgn**2, lgn_spikes_off_model_2, structure=lgn_structure_off, label='LGN_off')

lgn_neurons_on_3 = simulator.Population(Ncells_lgn**2, lgn_spikes_on_model_3, structure=lgn_structure_on, label='LGN_on')
lgn_neurons_off_3 = simulator.Population(Ncells_lgn**2, lgn_spikes_off_model_3, structure=lgn_structure_off, label='LGN_off')


# Spatial structure of cortical cells
lx = 0.75
ly = 0.75
x0 = -lx / 2
y0 = -ly / 2
dx = lx / (Ncell_exc - 1)
dy = ly / (Ncell_exc - 1)

excitatory_structure = space.Grid2D(aspect_ratio=1, x0=x0, y0=y0, dx=dx, dy=dy, z=0)
inhibitory_structure = space.Grid2D(aspect_ratio=1, x0=0, y0=0, dx=2*dx, dy=2*dy, z=0)

# Cortical parameters

# Common
Vth = -52.5  # mV
delay = 2.00  # ms

# Conductances
Vex = 0  # mV
Vin = -70  # mV
t_fall_exc = 1.75  # mV
t_fall_inh = 5.27  # mV


# Excitatory
C_exc = 0.500  # Nanofarads (500 Picofarads)
g_leak_exc = 0.025  # Microsiemens (25 Nanosiemens)
t_refrac_exc = 1.5  # ms
v_leak_exc = -73.6  # mV
v_reset_exc = -56.6  # mV
t_m_exc = C_exc / g_leak_exc  # Membrane time constant

# Inhibitory
C_inh = 0.214  # Nanofarads (214 Picofarads)
g_leak_inh = 0.018  # Microsiemens (18 Nanosiemens)
v_leak_inh = -81.6  # mV
v_reset_inh = -57.8  # mV
t_refrac_inh = 1.0  # ms
t_m_inh = C_inh / g_leak_inh  # Membrane time constant

# Cortical cell models
excitatory_cell = simulator.IF_cond_exp(tau_refrac=t_refrac_exc, cm=C_exc, tau_syn_E=t_fall_exc, v_rest=v_leak_exc,
                                        tau_syn_I=t_fall_inh, tau_m=t_m_exc, e_rev_E=Vex, e_rev_I=Vin, v_thresh=Vth,
                                        v_reset=v_reset_exc)

inhibitory_cell = simulator.IF_cond_exp(tau_refrac=t_refrac_inh, cm=C_inh, tau_syn_E=t_fall_exc, v_rest=v_leak_inh,
                                        tau_syn_I=t_fall_inh, tau_m=t_m_inh, e_rev_E=Vex, e_rev_I=Vin, v_thresh=Vth,
                                        v_reset=v_reset_inh)


# Cortical Population
cortical_neurons_exc = simulator.Population(1, excitatory_cell)
cortical_neurons_exc = simulator.Population(Ncell_exc**2, excitatory_cell, structure=excitatory_structure,
                                            label='Excitatory layer')
cortical_neurons_inh = simulator.Population(Ncell_inh**2, inhibitory_cell, structure=inhibitory_structure,
                                            label='Inhibitory layer')

#############################
# Add background noise
#############################

correlated = False
noise_rate = 5800  # Hz
g_noise = 0.00089 * 0  # Microsiemens (0.89 Nanosiemens)
noise_delay = 1  # ms
noise_model = simulator.SpikeSourcePoisson(rate=noise_rate)
noise_syn = simulator.StaticSynapse(weight=g_noise, delay=noise_delay)


if correlated:
    # If correlated is True all the cortical neurons receive noise from the same cell.
    noise_population = simulator.Population(1, noise_model, label='Background Noise')
    background_noise_to_exc = simulator.Projection(noise_population, cortical_neurons_exc,
                                                   simulator.AllToAllConnector(), noise_syn)
    background_noise_to_inh = simulator.Projection(noise_population, cortical_neurons_inh,
                                                   simulator.AllToAllConnector(), noise_syn)
else:
    # If correlated is False, all cortical neurons receive independent noise
    noise_population_exc = simulator.Population(Ncell_exc**2, noise_model, label='Background Noise to Exc')
    noise_population_inh = simulator.Population(Ncell_inh**2, noise_model, label='Background Noise to Inh')
    background_noise_to_exc = simulator.Projection(noise_population_exc, cortical_neurons_exc,
                                                   simulator.OneToOneConnector(), noise_syn)
    background_noise_to_inh = simulator.Projection(noise_population_inh, cortical_neurons_inh,
                                                   simulator.OneToOneConnector(), noise_syn)

#############################
## Thalamo-Cortical connections
#############################


# Sample random phases and orientations

phases_space = np.linspace(-180, 180, 20)
orientation_space = np.linspace(-90, 90, 20)

phases_exc = np.random.rand(Ncell_exc**2) * 360  # Phases continium
#phases_exc = np.random.choice(phases_space, Ncell_exc*2) # Phases discrete

orientations_exc = np.random.rand(Ncell_exc**2) * 180  # Orientations continium
orientations_exc = np.random.choice(orientation_space, Ncell_exc**2)   # Orientations discrete

phases_inh = np.random.rand(Ncell_inh**2) * 2 * np.pi
#phases_inh = np.random.choice(phases_space, Ncell_inh*2) # Phases discrete

orientations_inh = np.random.rand(Ncell_inh**2) * np.pi
orientations_inh = np.random.choice(orientation_space, Ncell_inh**2)  # Orientations discrete

w = 0.8  # Spatial frequency
gamma = 1  # Aspect ratio
sigma = 1  # Decay ratio
g_exc = 0.00098  # microsiemens
n_pick = 3  # Number of times to sample

polarity_on = 1
polarity_off = -1


if True:
    
    # LGN_on -> e  connection
    create_thalamocortical_connection(lgn_neurons_on, cortical_neurons_exc, polarity_on, n_pick, g_exc, 
                                      sigma, gamma, w, phases_exc, orientations_exc, simulator)
    # LGN_off - > e  connection
    create_thalamocortical_connection(lgn_neurons_off, cortical_neurons_exc, polarity_off, n_pick, g_exc, 
                                      sigma, gamma, w, phases_exc, orientations_exc, simulator)
    # LGN_on -> i  connection
    create_thalamocortical_connection(lgn_neurons_on, cortical_neurons_inh, polarity_on, n_pick, g_exc, 
                                      sigma, gamma, w, phases_exc, orientations_exc, simulator)
    # LGN_off -> i connection
    create_thalamocortical_connection(lgn_neurons_off, cortical_neurons_inh, polarity_off, n_pick, g_exc, 
                                      sigma, gamma, w, phases_exc, orientations_exc, simulator)

    
    

#############################
# Intracortical connections
#############################

# Connector parameters

n_pick = 10

orientation_sigma = np.pi * 0.25  # Decay in connectivity due to orientation differences
phase_sigma = np.pi * 0.75  # Decay in connectivity due to phase differences

# If true add cortical excitatory feedback (e -> e) and ( e -> i ) 
cortical_excitatory_feedback = True

## We create inhibitory feed-forward connections ( i -> e)   

# Create list of connections 
cortical_inh_exc_connections = create_cortical_to_cortical_connection(cortical_neurons_inh, cortical_neurons_exc,
                                                                      orientations_inh, phases_inh, orientations_exc,
                                                                      phases_exc, orientation_sigma, phase_sigma, g_exc,
                                                                      n_pick, target_type_excitatory=False)
# Make the list a connector
cortical_inh_exc_connector = simulator.FromListConnector(cortical_inh_exc_connections, column_names=["weight", "delay"])

# Projections
#cortical_inh_exc_projection = simulator.Projection(cortical_neurons_inh, cortical_neurons_exc,
#                                                   cortical_inh_exc_connector, receptor_type='inhibitory')

## Now we create the excitatory connections 
if cortical_excitatory_feedback:

    # Create list of connectors
    cortical_exc_exc_connections = create_cortical_to_cortical_connection(cortical_neurons_exc, cortical_neurons_exc,
                                                                          orientations_exc, phases_exc, orientations_exc,
                                                                          phases_exc, orientation_sigma, phase_sigma, g_exc,
                                                                          n_pick, target_type_excitatory=True)
    
    cortical_exc_inh_connections = create_cortical_to_cortical_connection(cortical_neurons_exc, cortical_neurons_inh,
                                                                          orientations_exc, phases_exc, orientations_inh,
                                                                          phases_inh, orientation_sigma, phase_sigma, g_exc,
                                                                          n_pick, target_type_excitatory=True)
    # Make the list a connector
    
    cortical_exc_exc_connector = simulator.FromListConnector(cortical_exc_exc_connections, column_names=["weight", "delay"])
    
    cortical_exc_inh_connector = simulator.FromListConnector(cortical_exc_inh_connections, column_names=["weight", "delay"])
    
    
    ## Projections
    cortical_exc_exc_projection = simulator.Projection(cortical_neurons_exc, cortical_neurons_exc,
                                                       cortical_exc_exc_connector, receptor_type='excitatory')
    
    cortical_exc_inh_projection = simulator.Projection(cortical_neurons_exc, cortical_neurons_inh,
                                                       cortical_exc_inh_connector, receptor_type='excitatory')


#############################n
# Recordings
#############################

lgn_neurons_on.record('spikes')
cortical_neurons_exc.record(['gsyn_exc', 'gsyn_inh'])


#############################
# Run model
#############################
simulator.run(t)  # Run the simulations for t ms
simulator.end()

#############################
# Extract the data
#############################

data = lgn_neurons_on.get_data()  # Creates a Neo Block
segment = data.segments[0]  # Takes the first segment          

data2 = cortical_neurons_exc.get_data()
segment2 = data2.segments[0]
g_exc = segment2.analogsignalarrays[0]
g_inh = segment2.analogsignalarrays[1]
#plt.plot(g_exc.times, np.mean(g_exc, axis=1))
#plt.plot(g_inh.times, -np.mean(g_inh, axis=1))

plt.plot(g_exc.times, g_exc[:, 0], label='Excitatory conductance')
plt.plot(g_inh.times, g_inh[:, 0], label='Inhibitory conductance')
plt.legend()

plt.show()

# Plot the spikes 

def plot_spiketrains(segment):
    for spiketrain in segment.spiketrains:
        y = np.ones_like(spiketrain) * spiketrain.annotations['source_id']
        plt.plot(spiketrain, y, '*b')
    plt.ylabel('Neuron number')
    plt.xlabel('Spikes')
        

#plot_spiketrains(segment)
#plt.show()

