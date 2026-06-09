import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as st
#显示中文
plt.rcParams['font.sans-serif'] = [u'SimHei']
plt.rcParams['axes.unicode_minus'] = False
fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(20, 8), dpi=100)
plt.subplot(221)
#绘制自由度为2的卡方分布的密度函数图像
df=2
a=1
lam=1/2
x= np.arange(0.01, 20, 0.01)
y1=st.chi2.pdf(x,df) 
plt.plot(x,y1,'r--',label='n={}'.format(df))
#绘制参数为α=1,λ=1/2的伽玛分布的密度函数图像
y2 = st.gamma.pdf(x,a, scale=1/lam) 
plt.plot(x, y2, 'b',label='α=1,λ=1/2')
plt.title('图a 伽玛分布的特例二：卡方分布')
plt.legend()
plt.grid()
plt.subplot(222)
#绘制自由度为2的卡方分布的密度函数图像
df=2
a=2
lam=1
x= np.arange(0.01, 20, 0.01)
y1=st.chi2.pdf(x,df) 
plt.plot(x,y1,'k--',label='n={}'.format(df))
#绘制参数为α=2,λ=1的伽玛分布的密度函数图像
y2 = st.gamma.pdf(x,a, scale=1/lam)
plt.plot(x, y2, 'b',label='α=2,λ=1')
plt.title('图b 伽玛分布的特例二：卡方分布')
plt.legend()
plt.grid()
plt.subplot(223)
#绘制卡自由度为1的卡方分布的密度函数图像
df=1
a=1
lam=1
x= np.arange(0.01, 20, 0.01)
y1=st.chi2.pdf(x,df) 
plt.plot(x,y1,'k--',label='n={}'.format(df))
#绘制参数为α=1,λ=1的伽玛分布的密度函数图像
y2 = st.gamma.pdf(x,a, scale=lam)
plt.plot(x, y2, 'b',label='α=1,λ=1')
plt.title('图c 伽玛分布的特例二：卡方分布')
plt.legend()
plt.grid()
plt.subplot(224)
#绘制自由度为1的卡方分布的密度函数图像
df=1
a=1/2
lam=1/2
x= np.arange(0.01, 20, 0.01)
y1=st.chi2.pdf(x,df) 
plt.plot(x,y1,'k--',label='n={}'.format(df))
#绘制参数为α=1/2,λ=1/2的伽玛分布的密度函数图像
y2 = st.gamma.pdf(x,a, scale=1/lam)  
plt.plot(x, y2, 'b',label='α=1/2,λ=1/2')
plt.title('图d 伽马分布的特例二：卡方分布')
plt.legend()
plt.grid()
plt.show()
