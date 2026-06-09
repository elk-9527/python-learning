from scipy.stats import geom
import matplotlib.pyplot as plt
import numpy as np
plt.rcParams['font.sans-serif'] = [u'SimHei']
plt.rcParams['axes.unicode_minus'] = False 
n=20
#求分布函数，并画图
fig,ax = plt.subplots(1,1)
p = 0.5
k = np.arange(0,n+1,1)
#求几何分布的分布函数
p1=geom.cdf(k, p)
#画出几何分布函数图像
ax.plot(k, p1,'o') 
plt.xlabel("k值")
plt.ylabel("概率")
plt.title("几何分布的分布函数,p=%.2f" % p)
plt.show()

