import numpy as np
from matplotlib import pyplot as plt
from scipy.integrate import quad
#一般的gamma函数
def gammafunc(a):
     y=lambda x: x**(a-1)*np.exp(-x)
     #此时有两个值，第一个值为积分值，第二个值为误差，只取第一个值即可。
     z1,z2=quad(y,0,np.inf) 
     return z1
#求gamma分布的密度函数
a=[1,2,5]
lamb=2   
for i in a:
    c = (lamb ** i) / gammafunc(i)
    x = np.arange(0, 20, 0.01, dtype=np.float)
    y = c * (x ** (i- 1)) * np.exp(-lamb * x)
    plt.plot(x, y, label=r'$\ \alpha=%.2f,\ \lambda=%.2f$' % (i, lamb))
plt.legend()
plt.show()
