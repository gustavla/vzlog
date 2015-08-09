from __future__ import division, print_function, absolute_import

import vzlog
import vzlog.pyplot as plt
import numpy as np

vz = vzlog.VzLog('log-image-grids')

vz.title('Image grids')

rs = np.random.RandomState(0)
x = rs.uniform(size=(9, 20, 20))

grid = vzlog.image.ImageGrid(x, cmap=plt.cm.rainbow)
grid.save(vz.impath('png'))

vz.text('You can scale the grid, creating a larger image:')
grid.save(vz.impath('png'), scale=3)

vz.text('Or, you can let your browser scale the image:')
grid.save(vz.impath('png', scale=3))
vz.text('Currently, only Firefox resizes this without blurring the image.')

vz.text('Use `ColorImageGrid` for RGB images:')
y = rs.uniform(size=(3, 20, 20, 3))
for i in range(3):
    y[i, ..., i] = 0

rgb_grid = vzlog.image.ColorImageGrid(y, rows=1)
rgb_grid.save(vz.impath('png', scale=3))

z = rs.uniform(size=(10, 10))
rgb_grid = vzlog.image.ImageGrid(z)
rgb_grid.save(vz.impath('png', scale=3))
