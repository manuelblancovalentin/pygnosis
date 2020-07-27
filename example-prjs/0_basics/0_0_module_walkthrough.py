""""""
""" Interactive plots """
import matplotlib
matplotlib.use('MacOSX')

""" Basic modules """
import numpy as np

""" Import PyGnosis """
import pygnosis

""" Set verbosity """
pygnosis.settings.VERBOSITY = 3

""" Create a System """
references = {'x': np.arange(0,1,.001),
              'y': np.arange(0,1,.001),
              'z': np.arange(0,1,.001)
              }

variables = {'T': [0.0, 0.0]}
sys = pygnosis.System(references, variables)

""" Now let's setup the dynamics of the system """
import tensorflow as tf
sigma = 1e-2
dTz_fun = lambda: tf.concat((sigma*(sys.T[:,:,1:] - sys.T[:,:,:-1]),sigma*tf.ones_like(sys.T[:,:,-2:-1])), axis = 2)
dynamics = {'T': dTz_fun}
sys.setup_dynamics(dynamics)

nsteps = 10
Ts = []
for _ in range(nsteps):
    current_state = sys()
    Ts.append(current_state['T'])









""" 
LORENTZ SYSTEM 
"""
""" Define parameters """
sigma = 10.0
rho = 28.0
beta = 8.0/3.0

""" Create PyGnosis System """
references = {}
variables = {'x': [1.0], # rate of convection, formally 'x'
             'y': [1.0], # horizontal temperature variation, formally 'y'
             'z': [1.0]  # vertical temperature variation, formally 'z'
             }
sys = pygnosis.System(references, variables)

""" Define system dynamics """
dx_dt = lambda: sigma*(sys.y - sys.x)
dy_dt = lambda: sys.x*(rho - sys.z) - sys.y
dz_dt = lambda: sys.x*sys.y - beta*sys.z
dynamics = {'x': dx_dt, 'y': dy_dt, 'z': dz_dt}
sys.setup_dynamics(dynamics)

""" Build simulation """
sim = pygnosis.Simulation(sys, timestep = 0.01, timespan = 40.0)

""" Run simulation """
states = sim()

""" Plot """
from matplotlib import cm
t = sim.time
ax, fig = sim.scatter('x','y','z', s = 1, c = cm.gnuplot2((t-t.min())/(t.ptp())))



