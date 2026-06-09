import numpy as np 
from scipy import stats  
import matplotlib.pyplot as plt  
#用来正常显示中文标签
plt.rcParams['font.sans-serif'] = [u'SimHei'] 
#用来正常显示正负号
plt.rcParams['axes.unicode_minus'] = False 
N=100
n=20
M=25
k= np.arange(0, 20,1)
s = stats.hypergeom.cdf(k,N,n,M)
plt.plot(k, s, marker='o', linestyle='None')
plt.xlabel("k值")
plt.ylabel("分布函数值")
plt.title("超几何分布的分布函数,N=%d,M=%d,n=%d" % (N, M, n))
plt.show()
