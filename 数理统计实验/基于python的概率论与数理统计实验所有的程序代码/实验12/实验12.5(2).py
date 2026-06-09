import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as st
fig=plt.figure()
ax=fig.add_subplot(1,1,1)
lam=1/2
x1= np.arange(1, 100, 1)
plt.ion()
for a in np.arange(10,0.5,-0.5):
    y1=st.chi2.pdf(x1,a)
    # 伽玛分布的参数为α,λ
    y2=st.gamma.pdf(x1,a/2,scale=1/lam)
    ax.cla()
    ax.plot(x1,y1,marker="*",color='b')
    ax.plot(x1,y2,marker=".",color='r')
    plt.pause(0.1)
