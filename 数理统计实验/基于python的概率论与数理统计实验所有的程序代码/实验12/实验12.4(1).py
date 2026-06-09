import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as st
#显示中文
plt.rcParams['font.sans-serif'] = [u'SimHei']
plt.rcParams['axes.unicode_minus'] = False
fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(20, 8), dpi=100)
plt.subplot(221)
#绘制λ=2指数分布的密度函数图像
lam=2
x= np.arange(0.01, 20, 0.01)
y1=st.expon.pdf(x,scale=lam) 
plt.plot(x,y1,'k--',label='λ={}'.format(lam))
#绘制α=2，λ=2的伽玛分布的密度函数图像
y2 = st.gamma.pdf(x,2, scale=2)#
plt.plot(x, y2, 'b',label='α=2,λ=2')
plt.title('图a 伽玛分布的特例一：指数分布')
plt.legend()
plt.grid()
plt.subplot(222)
#绘制λ=1指数分布的密度函数图像
lam=1
x= np.arange(0.01, 20, 0.01)
y1=st.expon.pdf(x,scale=lam) 
plt.plot(x,y1,'k--',label='λ={}'.format(lam))
#绘制α=2，λ=1的伽玛分布的密度函数图像
y2 = st.gamma.pdf(x,2, scale=1)
plt.plot(x, y2, 'b',label='α=2,λ=1')
plt.title('图b 伽玛分布的特例一：指数分布')
plt.legend()
plt.grid()
plt.subplot(223)
#绘制λ=2指数分布的密度函数图像
lam=2
x= np.arange(0.01, 20, 0.01)
y1=st.expon.pdf(x,scale=lam) 
plt.plot(x,y1,'k--',label='λ={}'.format(lam))
#绘制α=1，λ=2的伽玛分布的密度函数图像
y2 = st.gamma.pdf(x,1, scale=2)
plt.plot(x, y2, 'b',label='α=1,λ=2')
plt.title('图c 伽玛分布的特例一：指数分布')
plt.legend()
plt.grid()
plt.subplot(224)
#绘制λ=1指数分布的密度函数图像
lam=1
x= np.arange(0.01, 20, 0.01)
y1=st.expon.pdf(x,scale=lam) 
plt.plot(x,y1,'k--',label='λ={}'.format(lam))
#绘制α=1，λ=1的伽玛分布的密度函数图像
y2 = st.gamma.pdf(x,1, scale=1) 
plt.plot(x, y2, 'b',label='α=1,λ=1')
plt.title('图d 伽玛分布的特例一：指数分布')
plt.legend()
plt.grid()
plt.show()
