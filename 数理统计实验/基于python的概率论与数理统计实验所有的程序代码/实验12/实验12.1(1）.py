import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
#显示中文
plt.rcParams['font.sans-serif'] = [u'SimHei']
plt.rcParams['axes.unicode_minus'] = False
fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(20, 8), dpi=100)
plt.subplot(221)
# 绘制二项分布和泊松分布的分布律图像
n=10
p=0.5
lam=n*p
bino=stats.binom(n,p)
possion=stats.poisson(lam)
x1=np.arange(0,n)
y1=bino.pmf(x1)
plt.plot(x1,y1,'k--',label='n={},p={}'.format((n),(p)))
#绘制泊松分布的分布律图像
x2= np.arange(0,n)
y2 =possion.pmf(x2)
plt.plot(x2,y2,'b',label='λ={}'.format(lam))
plt.title('图a二项分布的泊松近似')
plt.legend()
plt.grid()
plt.subplot(222)
# 绘制二项分布的分布律图像
n=13
p=0.3
lam=n*p
bino=stats.binom(n,p)
possion=stats.poisson(lam)
x1=np.arange(0,n)
y1=bino.pmf(x1)
plt.plot(x1,y1,'k--',label='n={},p={}'.format((n),(p)))
#绘制泊松分布的分布律图像
x2= np.arange(0,n)
y2 =possion.pmf(x2)
plt.plot(x2,y2,'b',label='λ={}'.format(lam))
plt.title('图b 二项分布的泊松近似')
plt.legend()
plt.grid()
plt.subplot(223)
# 绘制二项分布的分布律图像
n=15
p=0.1
lam=n*p
bino=stats.binom(n,p)
possion=stats.poisson(lam)
x1=np.arange(0,n)
y1=bino.pmf(x1)
plt.plot(x1,y1,'k--',label='n={},p={}'.format((n),(p)))
#绘制泊松分布的分布律图像
x2= np.arange(0,n)
y2 =possion.pmf(x2)
plt.plot(x2,y2,'b',label='λ={}'.format(lam))
plt.title('图c二项分布的泊松近似')
plt.legend()
plt.grid()
plt.subplot(224)
# 绘制二项分布的分布律图像
n=20
p=0.05
lam=n*p
bino=stats.binom(n,p)
possion=stats.poisson(lam)
x1=np.arange(0,n)
y1=bino.pmf(x1)
plt.plot(x1,y1,'k--',label='n={},p={}'.format((n),(p)))
#绘制泊松分布分布律图像
x2= np.arange(0,n)
y2 =possion.pmf(x2)
plt.plot(x2,y2,'b',label='λ={}'.format(lam))
plt.title('图d二项分布的泊松近似')
plt.legend()
plt.grid()
plt.show()



