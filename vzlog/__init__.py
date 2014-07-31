from __future__ import division, print_function, absolute_import

from .vzlog import VzLog

VERSION = (0, 1, 0)
ISRELEASE = True
__version__ = '{0}.{1}.{2}'.format(*VERSION)
if not ISRELEASE:
    __version__ += '.git'
