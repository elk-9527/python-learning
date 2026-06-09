import numpy as np
from matplotlib import pyplot as plt
#使用公式求分布函数图像
def exponential(x, lamb):
    #指数分布的密度函数
    y = lamb * np.exp(-lamb * x) 
    return x, y
for lamb in [0.5, 1, 1.5]:
    x1 = np.arange(0, 20, 0.01, dtype=np.float)
    #计算指数分布的分布函数
    y1 = 1- np.exp(-lamb * x1) 
    #此处“%.2f”表示保留小数点后两位
    plt.plot(x1, y1,label=r'$\ \lambda=%.2f$' % (lamb)) 
plt.legend()
plt.show()

