from matplotlib import pyplot as plt
import numpy as np
import scipy.stats as st
fig=plt.figure()
ax=fig.add_subplot(1,1,1)
n=10
M =20
plt.ion()
x1=np.arange(0,n+1,1)
for N in range(50,300,10):
    p=M/N
    y1=st.binom.pmf(x1,n,p)
    y2=st.hypergeom.pmf(x1,N,M,n)
    ax.cla()
    ax.plot(x1,y1,marker="*",color='b')
    ax.plot(x1,y2,marker=".",color='r')
    plt.pause(0.1)
