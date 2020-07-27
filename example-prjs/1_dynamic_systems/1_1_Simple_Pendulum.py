
""" Import PyGnosis """
import pygnosis

""" Define parameters """
import numpy as np
theta0 = np.pi/8 #rads
L = .5 #meters
g = 9.81 #gravity
w = np.sqrt(g/L)
sigma = .2

""" Create PyGnosis System """
references = {}
variables = {'T': [-theta0]}
sys = pygnosis.System(references, variables)

""" Define system dynamics """
import tensorflow as tf
dT_dt = lambda: -theta0*w*tf.math.cos(w*sys.t)*tf.math.sin(w*sys.t)*tf.math.exp(-sigma*sys.t)
dynamics = {'T': dT_dt}
sys.setup_dynamics(dynamics)

""" Build simulation """
sim = pygnosis.Simulation(sys, with_respect_to = 't', timestep = 0.025, timespan = 20.0)

""" Run simulation """
states = sim()

""" Plot lines """
t = sim.time
ax, fig = sim.plot(t,'T')