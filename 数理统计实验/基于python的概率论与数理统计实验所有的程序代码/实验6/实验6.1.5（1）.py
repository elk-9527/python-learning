import numpy as np
from scipy.stats import gamma
from matplotlib import pyplot as plt
a=[1,2,5]
lamb=2   
for i in a:
    x = np.arange(0.5, 20, 0.01, dtype=np.float)
    y = gamma(i, 1/lamb).pdf(x)
    plt.plot(x, y, label=r'$\ \alpha1=%.2f,\ \lambda=%.2f$' % (i, lamb))
plt.legend()
plt.show()

