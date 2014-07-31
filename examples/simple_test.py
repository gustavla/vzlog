from __future__ import division, print_function, absolute_import 

from vzlog.default import vz

vz.title('My log file')

vz.section('Tests')

vz.text('Log some text.')

x = [1, 2, 3, 4]
vz.log('A list:', x)
