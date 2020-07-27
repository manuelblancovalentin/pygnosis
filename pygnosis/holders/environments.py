"""
ENVIRONMENTS BUILDER
PyGnosis v0.0.1

@author: Manu Blanco Valentin
@github: github.com/manuelblancovalentin
@email: manuel.blanco.valentin@gmail.com
"""

""" Basic modules """
import numpy as np
import tqdm as tqdm

""" Visualization """
import matplotlib.pyplot as plt

""" Tensorflow """
import tensorflow as tf

""" Import pygnosis for settings retrieval """
import pygnosis

""" Utils """
from ..utils import parsers

""" GENERAL PARAMETERS """
__DEFAULT_ENVIRONMENT_TIMESTEP__ = 1e-3
__DEFAULT_ENVIRONMENT_NUM_STEPS__ = 1e5

""" Definition of an simulation class """
class Simulation(object):
    def __init__(self, system, with_respect_to = None, **kwargs):
        """
        :param timestep: Time step in seconds. This parameter is used to compute the interactions between the
                         environment and any components inside it.
        """
        """ Super builder for forward compatibility """
        super().__init__()

        """ Init kwargs parser """
        kw_parser = parsers.KWARGS_PARSER(kwargs, raise_error = False)

        """ 
        Setup parameters in place 
        """

        """ Timing parameters """
        self.__setup_timing__(kw_parser)

        """ Environment Variables (which determine the state of the system at any given time) """
        self.states = {vn: np.zeros((self.num_steps+1,*system.vars[vn].shape.as_list())) for vn in system.vars}
        self.system = system


    """ Time property """
    @property
    def time(self):
        return np.arange(0, self.timespan, self.timestep)

    """ Call method (run simulation) """
    def __call__(self):

        """
        :return:
        """

        """ Store first element """
        for vn in self.states:
            self.states[vn][0] = getattr(self.system, vn).numpy()

        """ Loop thru all steps """
        for i, current_state in enumerate(tqdm.tqdm(self)):

            """ Set in place """
            if i < self.num_steps:
                for vn in self.states:
                    self.states[vn][i+1] = current_state[vn].numpy()

        return self.states

    """ length method """
    def __len__(self):
        return self.num_steps

    """ Iteration method """
    def __iter__(self):
        """
        :return:
        """
        """ Initialize iteration counter to zero """
        self.step = 0
        return self

    """ Next method """
    def __next__(self):
        """
        :return:
        """
        """ While step is inbounds """
        if self.step <= self.num_steps:

            """ Compute current_state for systems inside environment """
            current_state, _ = self.system(self.timestep)

            if hasattr(self.system,'t'):
                getattr(self.system,'t').assign([self.timestep*self.step])

            self.step += 1
            return current_state
        else:
            raise StopIteration

    """ Setup timing """
    def __setup_timing__(self, kw_parser):
        """
        :param kw_parser:
        :return:
        """

        """ Init timer to zero """
        self.step = 0

        """ Init timing parameters """
        self.timestep = kw_parser.__has_entry__('timestep', None, rule=kw_parser.is_num)
        self.timespan = kw_parser.__has_entry__('timespan', None, rule=kw_parser.is_num)
        self.num_steps = kw_parser.__has_entry__('num_steps', None, rule=kw_parser.is_num)
        if self.num_steps is None:
            if self.timespan is None:
                if self.timestep is None:
                    self.timestep = __DEFAULT_ENVIRONMENT_TIMESTEP__
                    extra = ' default'

                self.num_steps = int(__DEFAULT_ENVIRONMENT_NUM_STEPS__)
                self.timespan = int(self.timestep * self.num_steps)

                pygnosis.settings.LOG_HISTORY('info', f'Environment timestep set to{extra} value: {self.timestep}')
                pygnosis.settings.LOG_HISTORY('info', f'Environment num_steps set to default value: {self.num_steps}')
                pygnosis.settings.LOG_HISTORY('info', f'Environment timespan set to calculated value: {self.timespan}')

            else:
                extra = ''
                if self.timestep is None:
                    self.timestep = __DEFAULT_ENVIRONMENT_TIMESTEP__
                    extra = ' default'

                pygnosis.settings.LOG_HISTORY('info', f'Environment timestep set to{extra} value: {self.timestep}')

                if self.timestep <= self.timespan:
                    self.num_steps = int(self.timespan // self.timestep)
                    extra = 'set'
                    type = 'info'
                else:
                    self.num_steps = 1
                    self.timespan = int(self.timestep * self.num_steps)
                    extra = 'changed'
                    type = 'warning'

                pygnosis.settings.LOG_HISTORY(type, f'Environment num_steps {extra} to value: {self.num_steps}')
                pygnosis.settings.LOG_HISTORY(type, f'Environment timespan {extra} to value: {self.timespan}')

        else:
            if self.timespan is None:
                if self.timestep is None:
                    self.timestep = __DEFAULT_ENVIRONMENT_TIMESTEP__
                    extra = ' default'

                self.timespan = int(self.timestep * self.num_steps)

                pygnosis.settings.LOG_HISTORY('info', f'Environment timestep set to{extra} value: {self.timestep}')
                pygnosis.settings.LOG_HISTORY('info', f'Environment num_steps set to default value: {self.num_steps}')
                pygnosis.settings.LOG_HISTORY('info', f'Environment timespan set to calculated value: {self.timespan}')

            else:
                self.timestep = self.timespan / self.num_steps
                extra = ' calculated'

                pygnosis.settings.LOG_HISTORY('info', f'Environment timestep set to{extra} value: {self.timestep}')
                pygnosis.settings.LOG_HISTORY('info', f'Environment num_steps set to default value: {self.num_steps}')
                pygnosis.settings.LOG_HISTORY('info', f'Environment timespan set to calculated value: {self.timespan}')


    """ PLOT METHODS """
    def __plotter__(self, plot_fn, *vars, projection = None, **plt_kwargs):
        """
        :param vars:
        :param projection:
        :param plt_kwargs:
        :return:
        """
        """ Make sure we only have at most 3 vars to plot """
        if (len(vars) > 3) and plot_fn in ('scatter'):
            pygnosis.settings.LOG_HISTORY('error',
                                          f'Too many variables to plot. Maximum number is 3 but a total of {len(vars)} were passed.')

        if projection not in pygnosis.settings.VALID_PYPLOT_PROJECTIONS:
            pygnosis.settings.LOG_HISTORY('warning',
                                          f'Invalid projection {projection}. Valid types are: {", ".join(pygnosis.settings.VALID_PYPLOT_PROJECTIONS)}. '\
                                          f'Setting to default "None" and proceeding.')

            projection = None

        if projection is None:
            """ Deduce from len(vars) """
            if len(vars) == 3 and plot_fn != 'plot':
                projection = '3d'

        """ Get states for each var """
        var_names = vars
        vars = [self.states[vn] if isinstance(vn,str) else vn for vn in vars]

        """ Init figure """
        fig = plt.figure()
        ax = fig.gca(projection = projection)

        """ Build plot """
        art = getattr(ax,plot_fn)(*vars, **plt_kwargs)
        if plot_fn == 'plot':
            plt.legend(iter(art), [var_names[2*i+1] for i in range(int(len(vars)//2))])

        """ Return axis and figure """
        return fig, ax

    """ Plot methods """
    def scatter(self, *vars, projection = None, **plt_kwargs):
        return self.__plotter__('scatter', *vars, projection = projection, **plt_kwargs)


    """ Plot method """
    def plot(self, *vars, projection = None, **plt_kwargs):
        return self.__plotter__('plot', *vars, projection = projection, **plt_kwargs)



"""  (dynamic) System definition """
class System(tf.Module):
    def __init__(self, references: dict, variables: dict):
        """
        :param references: Dictionary containing entries for each one of the ref space variables (invariant)
                            i.e., {'x': np.arange(0,1,.1), 'y': np.arange(0,2,.2)}
                            OR
                            Dictionary containing Reference objects for each entry in ref space variables
        """

        """ Create References for all variables in references """
        __refs__ = dict()

        """ If references are empty, add time """
        if len(references) == 0:
            references = {'t': 0.0}

        """ Create meshgrid first """
        mesh = np.meshgrid(*tuple([references[vn] for vn in references]))
        for ivn, vn in enumerate(references):
            ref = references[vn]
            if not isinstance(ref, tf.Variable):
                ref = tf.Variable(mesh[ivn], name = vn, dtype = 'float64')
            __refs__[vn] = ref

            """ Make sure to link attribute 'vn' in the Module so we can access it later """
            setattr(self, vn, ref)

        self.references = __refs__

        """ Get mesh shape """
        mesh_shape = mesh[0].shape if len(mesh) > 0 else ()

        """ Check if varibles is subscriptable """
        if not hasattr(variables, '__getitem__'):
            variables = {vn: [np.zeros(mesh_shape)] for vn in variables}

        """ Create holders for variables """
        __vars__ = dict()
        __grads__= dict()
        for vn in variables:
            var = variables[vn]
            if not isinstance(var, tf.Variable):
                var_init = var[0]
                if np.shape(var_init) != mesh_shape:
                    var_init = np.zeros(mesh_shape)
                _var_ = tf.Variable(var_init, name = vn, dtype = 'float64')
                order = len(var)
            else:
                _var_ = var[0]
                order = var[1]

            __vars__[vn] = _var_
            """ Make sure to link attribute 'vn' in the Module so we can access it later """
            setattr(self,vn,_var_)

            """ Create gradientTape to compute (if necessary) """
            for n in range(1,order):
                grad_name = f'd{n if n > 1 else ""}{vn}_dt{n if n > 1 else ""}'
                if not isinstance(var[n], tf.Variable):
                    grad_init = var[n]
                    if np.shape(grad_init) != mesh_shape:
                        grad_init = np.zeros(mesh_shape)
                    _grad_ = tf.Variable(grad_init,
                                         name = grad_name,
                                         dtype = 'float64')
                else:
                    _grad_ = var[n]
                """ Setup in place """
                __grads__[vn] = _grad_

                """ Make sure to link attribute 'vn' in the Module so we can access it later """
                setattr(self, grad_name, _grad_)

        self.vars = __vars__
        self.grads = __grads__

        """ Init dynamics """
        self.setup_dynamics(dict())

    """ Define dynamics """
    def setup_dynamics(self, dynamics: dict):
        """
        :param dynamics:
        :return:
        """

        """ Parse dynamics """
        if dynamics is not None and not isinstance(dynamics, dict):
            dynamics = None
        if dynamics is None:
            dynamics = {vn: lambda: 0.0 for vn in dynamics}

        """ Check we have an entry for each variable in init_state """
        for vn in self.vars:
            if vn not in dynamics:
                dynamics[vn] = lambda: 0.0
        self.dynamics = dynamics

        """ Make tf.functions """
        #self.dynamics = {vn: tf.function(self.dynamics[vn]) for vn in self.dynamics}

        """ Create gradients """
        #tf.GradientTape(persistent=True)

    """ Call to compute next state """
    def __call__(self, dt, perturbations = None):
        """
        :param perturbations:
        :return:
        """
        """ Parse init_state """
        if perturbations is not None and not isinstance(perturbations, dict):
            perturbations = None
        if perturbations is None:
            perturbations = {vn: tf.zeros_like(self.vars[vn]) for vn in self.vars}

        """ Check we have an entry for each variable in init_state """
        perturbations = {vn: tf.zeros_like(self.vars[vn]) if vn not in perturbations else perturbations[vn] for vn in self.vars}

        """ Compute deltas """
        __deltas__ = dict()
        for vn in self.vars:
            __deltas__[vn] = dt*self.dynamics[vn]().numpy()

        """ Now apply deltas """
        for vn in self.vars:
            self.vars[vn].assign_add(__deltas__[vn])
            self.vars[vn].assign_add(perturbations[vn].numpy())

        return self.vars, __deltas__

    """ Add method """
    def __add__(self, system):
        """
        :param system: New system of class System to be added to current
        :return: a new System object
        """

