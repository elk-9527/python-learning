import numpy as np 
from scipy import stats  
import matplotlib.pyplot as plt  
plt.rcParams['font.sans-serif'] = [u'SimHei'] 
plt.rcParams['axes.unicode_minus'] = False 
N=100
n=20
M=25
k= np.arange(0, 20,1)
#求超几何分布的分布律值并画图
p = stats.hypergeom.pmf(k,N,n,M)
plt.plot(k, p, marker='o', linestyle='None')
plt.xlabel("k值")
plt.ylabel("概率")
plt.title("超几何分布的分布律,N=%d,M=%d,n=%d" % (N, M, n))
plt.show()

