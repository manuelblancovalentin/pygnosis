"""
SETTINGS
PyGnosis v0.0.1

@author: Manu Blanco Valentin
@github: github.com/manuelblancovalentin
@email: manuel.blanco.valentin@gmail.com
"""

""" 
DISPLAY OPTIONS 
"""

""" Verbosity: 
        0 -: Nothing is displayed
        1 -: Only errors are displayed
        2 -: Errors & Warnings are displayed
        3 -: Errors & Warnings & Logs are displayed
"""
VERBOSITY = 3

""" 
HOLDERS 
"""

""" Create log object to keep track of warnings, errors, etc. """
from .utils.logging import LOG
LOG_HISTORY = LOG()

""" Valid projections for matplotlib plotting """
VALID_PYPLOT_PROJECTIONS = {None, 'aitoff', 'hammer', 'lambert', 'mollweide', 'polar', 'rectilinear'}
