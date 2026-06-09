#此程序只能求参数为正整数时贝塔分布的密度函数
import numpy as np
from matplotlib import pyplot as plt
#求阶乘，即gamma（n）
def gamma_function(n):
    s = 1
    for i in range(2, n):
        s *= i
    return s
#利用密度函数公式画出图形
for ls in [(1, 1), (1, 2), (2, 1), (2, 2)]:
    alpha, beta = ls[0], ls[1]
    gamma = gamma_function(alpha + beta) / (gamma_function(alpha) * gamma_function(beta))
    x = np.arange(0, 1, 0.001, dtype=np.float)
    y = gamma * (x ** (alpha - 1)) * ((1 - x) ** (beta - 1))
    plt.plot(x, y, label=r'$\ \alpha=%d,\ \beta=%d$' % (alpha, beta))
plt.legend()
plt.show()
