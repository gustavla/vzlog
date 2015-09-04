from __future__ import division, print_function, absolute_import

from vzlog.vzlog import VzLog
from vzlog import image

VERSION = (0, 1, 7)
ISRELEASE = True
__version__ = '{0}.{1}.{2}'.format(*VERSION)
if not ISRELEASE:
    __version__ += '.git'

__all__ = ['VzLog', 'image', '__version__']
