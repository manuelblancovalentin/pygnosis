
""" Import PyGnosis """
import pygnosis

import numpy as np

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