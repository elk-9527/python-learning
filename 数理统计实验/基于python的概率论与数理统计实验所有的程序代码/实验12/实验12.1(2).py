from matplotlib import pyplot as plt
import numpy as np
from scipy import stats
fig=plt.figure()
ax=fig.add_subplot(1,1,1)
plt.ion()
n=200
for p in np.arange(0.5,0.05,-0.05):
        x1=np.arange(0,n)
        y1=stats.binom.pmf(x1,n,p)
        y2=stats.poisson.pmf(x1,n*p)
        ax.cla()
        ax.plot(x1,y1,marker="*",color='b')
        ax.plot(x1,y2,marker="*",color='r')
        plt.pause(0.1)

