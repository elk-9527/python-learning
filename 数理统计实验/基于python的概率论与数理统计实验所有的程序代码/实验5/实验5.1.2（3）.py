from matplotlib import pyplot as plt
import numpy as np
#用来正常显示中文标签
plt.rcParams['font.sans-serif'] = [u'SimHei'] 
#用来正常显示正负号
plt.rcParams['axes.unicode_minus'] = False 
#计算阶乘，定义阶乘函数为factorial
def factorial(n):
    s=1
    for i in range(1,n+1):
        s=s*i
    return s
lamb=0.5
s=0
n=20
#计算泊松分布的分布律
for k in range(0,n+1):
    #计算泊松分布的分布律
    p=lamb**k*np.exp(-lamb)/factorial(k) 
    #泊松分布的分布律值并画图
    plt.plot(k, p,linestyle='', marker='.')  
    plt.xlabel("k值")
    plt.ylabel("概率")
    plt.title("泊松分布的分布律，λ=%.2f" % lamb)
plt.show()
