from vzlog import VzLog
import matplotlib as mpl
mpl.use('Agg')
mpl.rc('font', size=8)
import pylab as pl
import numpy as np

vz = VzLog('log')

vz.title('VzLog')
vz.text(u'Goals'.encode('utf-8'))
vz.items(['Rich logging', 'Avoid annoying pop-up windows'])

vz.section('A plot')
x = np.linspace(0, 2*np.pi)
fig = pl.figure(figsize=(4, 3))
pl.plot(x, np.sin(x))
pl.xlim((0, 2*np.pi))
pl.savefig(vz.impath('svg'))

np.set_printoptions(precision=1)
vz.log(x)
