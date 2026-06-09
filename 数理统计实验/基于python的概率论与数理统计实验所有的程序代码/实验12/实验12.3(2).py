import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
fig=plt.figure()
ax=fig.add_subplot(1,1,1)
mu=0
sigma=1
plt.ion()
x1 = np.linspace(-5,5,50)
for df in range(1,30,1):
    y1=stats.norm.pdf(x1,mu,sigma)
    y2=stats.t.pdf(x1,df)
    ax.cla()
    ax.plot(x1,y1,marker="*",color='b', label='标准正态分布')
    ax.plot(x1,y2,marker=".",color='k' ,label='t分布')
    plt.pause(0.1)
