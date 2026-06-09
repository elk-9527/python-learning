import numpy as np
from scipy.stats import expon
from matplotlib import pyplot as plt
#使用统计包画密度函数图像
for lamb in [0.5, 1, 1.5]:
    x = np.arange(0, 20, 0.01, dtype=np.float)
    y= expon.pdf(x, scale=lamb)
    plt.plot(x, y, label=r'$\ \lambda=%.2f$' % (lamb))
plt.legend()
plt.show()

