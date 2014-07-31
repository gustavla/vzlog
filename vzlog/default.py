from __future__ import division, print_function, absolute_import 

import os
from vzlog import VzLog

__all__ = ['vz']

_DEFAULT_NAME = os.environ.get('VZ_NAME', 'vzlog')
_vz_dir = os.environ.get('VZ_DIR', '')
_DEFAULT_ROOT = os.path.expandvars(os.path.expanduser(_vz_dir))
_DEFAULT_FILE_RIGHTS = os.environ.get('VZ_FILE_RIGHTS')

# Construct default VzLog object
vz = VzLog(os.path.join(_DEFAULT_ROOT, _DEFAULT_NAME),
           file_rights=_DEFAULT_FILE_RIGHTS)
