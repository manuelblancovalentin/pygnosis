"""
LOGGING
PyGnosis v0.0.1

@author: Manu Blanco Valentin
@github: github.com/manuelblancovalentin
@email: manuel.blanco.valentin@gmail.com
"""

""" Basic modules """
from datetime import datetime

""" PyGnosis for settings """
import pygnosis

""" Message types def """
class MESSAGE():
    def __init__(self, message: str):
        super().__init__()
        self.message = message
        self.time = datetime.now()
        self.printed = False


class ERROR(MESSAGE):
    def __init__(self, message: str):
        super().__init__(message)
        self.prefix = 'ERROR'
        self.min_verbosity =  1

class WARNING(MESSAGE):
    def __init__(self, message: str):
        super().__init__(message)
        self.prefix = 'WARNING'
        self.min_verbosity = 2

class INFO(MESSAGE):
    def __init__(self, message: str):
        super().__init__(message)
        self.prefix = 'INFO'
        self.min_verbosity = 3

__LOG_TYPES__ = {'error': ERROR,
                 'warning': WARNING,
                 'info': INFO,
                 ERROR: ERROR,
                 WARNING: WARNING,
                 INFO: INFO
                 }


""" LOG CLASS """
class LOG():
    def __init__(self):
        super().__init__()
        self.stack = []

    def __call__(self, type: str, message: str):
        """
        :param type: either ERROR, WARNING or INFO
        :param message: string
        :return:
        """

        """ Create object """
        msg = __LOG_TYPES__.get(type.lower(), 'info')(message)

        """ Stack """
        self.stack.append(msg)

        """ print according to verbosity """
        if pygnosis.settings.VERBOSITY >= msg.min_verbosity:
            msg_txt = f'@{msg.time.strftime("%H:%M:%S")} [{msg.prefix}] - {msg.message}'
            msg.printed = True
            if isinstance(msg,ERROR):
                raise ValueError(msg_txt)
            else:
                print(msg_txt)





