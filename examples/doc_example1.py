from vzlog import VzLog
import vzlog.pyplot as plt
import numpy as np

vz = VzLog('log')

vz.title('VzLog')
vz.text('Goals')
vz.items(['Rich logging', 'Avoid annoying pop-up windows'])

vz.section('A plot')
x = np.linspace(0, 2*np.pi)
fig = plt.figure(figsize=(4, 3))
plt.plot(x, np.sin(x))
plt.xlim((0, 2*np.pi))
plt.savefig(vz.impath('svg'))

np.set_printoptions(precision=1)
vz.log(x)
