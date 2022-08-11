import matplotlib.pyplot as plt
import numpy as np


def discrete_matshow(data):
    # get discrete colormap
    cmap = plt.get_cmap('RdBu', np.max(data) - np.min(data) + 1)
    # set limits .5 outside true range
    mat = plt.matshow(data, cmap=cmap, vmin=np.min(data) - 0.5, 
                      vmax=np.max(data) + 0.5, fignum=111)
    # tell the colorbar to tick at integers
    cax = plt.colorbar(mat, ticks=np.arange(np.min(data), np.max(data) + 1))

# generate data
a = np.random.randint(1, 9, size=(100, 100))
discrete_matshow(a)
fig2 = plt.figure(112)
y = np.random.random([10,1])
plt.plot(y)

plt.show()