import numpy as np
from scipy.stats import expon
from matplotlib import pyplot as plt
for lamb in [0.5, 1, 1.5]:
    x = np.arange(0, 20, 0.01, dtype=np.float)
    #用scipy.stats.expon工具箱,注意这里的scale参数是标准差
    y= expon.cdf(x, scale=1/lamb) 
    plt.plot(x, y, label=r'$\ \lambda=%.2f$' % (lamb))
#调整标签的大小和位置
plt.legend(loc='upper right',fontsize=10) 
plt.show()


