from scipy import stats
import matplotlib.pyplot as plt
import numpy as np
#参数取值为1，2
m = [1, 2]
x = np.linspace(0, 1, 100)
for i in range(2):
  for j in range(2):
    alpha = m[i]
    beta = m[j]
    y = stats.beta(alpha, beta).cdf(x)
    plt.plot(x, y, label=r'$\ \alpha=%.1f,\ \beta=%.1f$' % (alpha, beta))
#调整标签的大小和位置
plt.legend(loc='upper left',fontsize=10) 
plt.show()

