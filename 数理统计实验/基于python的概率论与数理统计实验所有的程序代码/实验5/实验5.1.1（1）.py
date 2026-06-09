from scipy.stats import binom
import matplotlib.pyplot as plt
import numpy as np
#用来正常显示中文标签
plt.rcParams['font.sans-serif'] = [u'SimHei'] 
#用来正常显示正负号
plt.rcParams['axes.unicode_minus'] = False 
fig,ax = plt.subplots(1,1)
n = 60
p = 0.5
x = np.arange(0,60)
ax.plot(x, binom.pmf(x, n, p),'o')
plt.title("二项分布的分布律，n=%d,p=%.2f" % (n,p))
plt.show()
