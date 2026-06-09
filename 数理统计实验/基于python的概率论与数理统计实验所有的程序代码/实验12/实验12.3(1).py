import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
#显示中文
plt.rcParams['font.sans-serif'] = [u'SimHei']
plt.rcParams['axes.unicode_minus'] = False
fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(20, 8), dpi=100)
plt.subplot(221)
mu=0
sigma=1
# 绘制标准正态分布的密度函数图像
x = np.linspace(-5,5,10000)
y1 = stats.norm.pdf(x,mu,sigma)
plt.plot(x,y1,'b',label='mμ={},σ={}'.format((mu),(sigma)))
#绘制自由度为1的t分布的密度函数图像 
df=1
y2= stats.t.pdf(x,df)
plt.plot(x,y2,'k--',label='n={}'.format(df))
plt.title('图a t分布的正态近似')
plt.legend()
plt.grid()
plt.subplot(222)
mu=0
sigma=1
# 绘制标准正态分布的密度函数图像
x = np.linspace(-5,5,10000)
y1 = stats.norm.pdf(x,mu,sigma)
plt.plot(x,y1,'b',label='μ={},σ={}'.format((mu),(sigma)))
#绘制自由度为10的t分布的密度函数图像
df=10
y2= stats.t.pdf(x,df)
plt.plot(x,y2,'k--',label='n={}'.format(df))
plt.title('图b t分布的正态近似')
plt.legend()
plt.grid()
plt.subplot(223)
mu=0
sigma=1
# 绘制标准正态分布的密度函数图像
x = np.linspace(-5,5,10000)
y1 = stats.norm.pdf(x,mu,sigma)
plt.plot(x,y1,'b',label='μ={},σ={}'.format((mu),(sigma)))
#绘制自由度为20的t分布的密度函数图像
df=20
y2= stats.t.pdf(x,df)
plt.plot(x,y2,'k--',label='n={}'.format(df))
plt.title('图c t分布的正态近似')
plt.legend()
plt.grid()
plt.subplot(224)
mu=0
sigma=1
# 绘制标准正态分布的密度函数图像
x = np.linspace(-5,5,10000)
y1 = stats.norm.pdf(x,mu,sigma)
plt.plot(x,y1,'b',label='μ={},σ={}'.format((mu),(sigma)))
#绘制自由度为30的t分布的密度函数图像
df=30
y2= stats.t.pdf(x,df)
plt.plot(x,y2,'k--',label='n={}'.format(df))
plt.title('图d t分布的正态近似')
plt.legend()
plt.grid()
plt.show()
