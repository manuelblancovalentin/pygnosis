
"""
LORENTZ SYSTEM
"""

""" Import PyGnosis """
import pygnosis

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

""" 3-D Scatter """
from matplotlib import cm
t = sim.time
ax, fig = sim.scatter('x','y','z', s = 1, c = cm.gnuplot2((t-t.min())/(t.ptp())))

""" Plot lines """
ax, fig = sim.plot(t,'x',t,'y',t,'z')