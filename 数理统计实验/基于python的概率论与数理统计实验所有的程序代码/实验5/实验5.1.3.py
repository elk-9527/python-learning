from scipy.stats import binom
from scipy.stats import poisson
import matplotlib.pyplot as plt
import numpy as np
plt.rcParams['font.sans-serif'] = [u'SimHei'] 
plt.rcParams['axes.unicode_minus'] = False
fig,ax = plt.subplots(1,1)	 
n = 500
p = 0.1
x = np.arange(0,120,1)
p1, = ax.plot(x, binom.pmf(x, n, p),'b*',label =u'二项分布')
mu = n*p
p2, = ax.plot(x, poisson.pmf(x, mu),'ro',label = u'泊松分布')
plt.legend(handles = [p1, p2])
plt.title(u'泊松分布和二项分布对比')
plt.show()

