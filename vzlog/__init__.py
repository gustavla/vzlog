from __future__ import division, print_function, absolute_import

import os
from .vzlog import VzLog

_DEFAULT_NAME = os.environ.get('VZ_DEFAULT_NAME', 'vzlog')

# The default singleton VzLog
default = VzLog(_DEFAULT_NAME)
