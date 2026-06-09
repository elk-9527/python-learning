import numpy as np
from matplotlib import pyplot as plt
def exponential(x, lamb):
    y = lamb * np.exp(-lamb * x)
    return x, y
for lamb in [0.5, 1, 1.5]:
    x = np.arange(0, 20, 0.01, dtype=np.float)
    x, y= exponential(x, lamb)
    plt.plot(x, y,label=r'$\ \lambda=%.2f$' % (lamb))
plt.legend()
plt.show()
