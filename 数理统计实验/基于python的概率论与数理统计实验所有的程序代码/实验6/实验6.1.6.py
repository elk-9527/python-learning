import numpy as np
from matplotlib import pyplot as plt
#求当n为正整数时的gamma函数
def gamma_function(n):
  s = 1
  for i in range(2, n):
      s *= i
  return s
#对三对参数分别画出gamma分布的密度函数图像
Z=[ (3, 0.5) , (3, 2), (3, 5)]
for l in Z:
    a, lamb = l[0], l[1]
    c = (lamb ** a) / gamma_function(a)
    x = np.arange(0, 20, 0.01, dtype=np.float)
    y = c * (x ** (a - 1)) * np.exp(-lamb * x)
    plt.plot(x, y, label=r'$\ \alpha=%.2f,\ \lambda=%.2f$' % (a, lamb))
plt.legend()
plt.show()

