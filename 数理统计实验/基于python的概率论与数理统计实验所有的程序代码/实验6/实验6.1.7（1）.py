#使用统计软件包
from scipy import stats
import matplotlib.pyplot as plt
import numpy as np
#参数取值为1，2
m = [1,2]
x = np.linspace(0, 1, 100)
for i in range(2):
  for j in range(2):
    alpha = m[i]
    beta = m[j]
    y = stats.beta(alpha, beta).pdf(x)
    plt.plot(x, y, label=r'$\ \alpha=%d,\ \beta=%d$' % (alpha, beta))
plt.legend()
plt.show()

