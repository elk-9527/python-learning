import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as st
fig=plt.figure()
ax=fig.add_subplot(1,1,1)
lam=1
x1= np.arange(1, 100, 2)
plt.ion()
for a in np.arange(10,1,-1):
    y1=st.expon.pdf(x1,scale=lam)
    y2=st.gamma.pdf(x1,a,scale=1/lam)
    ax.cla()
    ax.plot(x1,y1,marker="*",color='b')
    ax.plot(x1,y2,marker=".",color='k')
    plt.pause(0.1)

