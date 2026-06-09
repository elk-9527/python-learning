import numpy as np
import math
from matplotlib import pyplot as plt
from scipy.integrate import quad
#一般的gamma函数，求积分
def gammafunc(a):
    y=lambda x: x**(a-1)*math.exp(-x)
    #此时有两个值，第一个值为积分值，第二个值为误差，只取第一个值即可
    z1,z2=quad(y,0,np.inf) 
    return z1
for ls in [(1.5, 1), (1.5, 2.5), (1.5, 3), (1.5, 4.5)]:
    alpha, beta = ls[0], ls[1]
    x = np.arange(0, 1, 0.001, dtype=np.float)
    gamma = gammafunc(alpha + beta) / (gammafunc(alpha) *gammafunc(beta))
    y = gamma * (x ** (alpha - 1)) * ((1 - x) ** (beta - 1))
    plt.plot(x, y, label=r'$\ \alpha=%.1f,\ \beta=%.1f$' % (alpha, beta))
plt.legend()
plt.show()

