"""
PARSERS
PyGnosis v0.0.1

@author: Manu Blanco Valentin
@github: github.com/manuelblancovalentin
@email: manuel.blanco.valentin@gmail.com
"""

""" Import pygnosis for settings retrieval """
import pygnosis

""" 
PARSING GENERAL RULES 
"""

""" Check if variable is number (float, integer ...) """
def is_num(value):
    if isinstance(value, (float, int)):
        return True
    elif isinstance(value, str):
        return value.isnumeric()
    else:
        try:
            float(value)
            return True
        except:
            return False


"""
KW_PARSER class. 
"""
class KWARGS_PARSER(object):
    def __init__(self, kwargs, raise_error = False):
        """
        :param kwargs: kwargs dict to be parsed
        :param raise_error: flag to indicate whether to raise assertion error when checking the rule on __has_entry__
                            method or not.
        """
        super().__init__()
        self.kwargs = kwargs
        self.raise_error = raise_error

        """ Definition of parse general functions """
        self.is_num = is_num

    """ Has entry method """
    def __has_entry__(self, entry, default = None, rule = lambda x: True):

        if entry in self.kwargs:
            value = self.kwargs[entry]
            extra = ' (found in kwargs)'
        else:
            value = default
            extra = ' (default value)'

        """ Check rule """
        if not rule(value):
            if self.raise_error:
                raise ValueError(f'Invalid type of variable found for entry {entry}: {value}. If you wish to skip this '\
                                 f'type of error, initialize the kw_parser using "raise_error = False".')

            else:
                pygnosis.settings.LOG_HISTORY('warning', f'Invalid type of variable found for entry {entry}: {value}.')

        else:
            pygnosis.settings.LOG_HISTORY('info', f'Value for {entry} set to {value}{extra}.')

        """ Set value in place """
        self.kwargs[entry] = value

        """ Return value """
        return value





