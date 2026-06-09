from matplotlib import pyplot as plt
import numpy as np
from scipy import stats
plt.rcParams['font.sans-serif'] = [u'SimHei']
plt.rcParams['axes.unicode_minus'] = False
fig=plt.figure()
ax=fig.add_subplot(1,1,1)
lam=1
plt.ion()
x1=np.arange(0,40)
for n in range(0,30,1):
    y1=stats.poisson.pmf(x1,n*lam)
    y2=stats.norm.pdf(x1,n*lam,np.sqrt(n*lam))
    ax.cla()
    ax.plot(x1,y1,"r--",label=r'泊松分布')
    ax.plot(x1,y2,color='b',label=r'正态分布')
    #调整标签的大小和位置
    plt.legend(loc='upper right',fontsize=10) 
    plt.pause(0.1)


