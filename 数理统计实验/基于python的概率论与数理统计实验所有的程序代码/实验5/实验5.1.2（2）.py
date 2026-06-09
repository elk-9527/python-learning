import numpy as np 
# 统计计算包的统计模块
from scipy import stats  
# 绘图包
import matplotlib.pyplot as plt  
#用来正常显示中文标签
plt.rcParams['font.sans-serif'] = [u'SimHei'] 
#用来正常显示正负号
plt.rcParams['axes.unicode_minus'] = False 
lamb=0.5
k= np.arange(0, 20,1)
#计算泊松分布的分布函数值并画图
s = stats.poisson.cdf(k,lamb)
plt.plot(k, s, marker='o', linestyle='None')
plt.xlabel("k值")
plt.ylabel("分布函数值")
plt.title("泊松分布的分布函数，λ=%.2f" % lamb)
plt.show()

