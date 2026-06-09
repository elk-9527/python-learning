import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as st
#显示中文
plt.rcParams['font.sans-serif'] = [u'SimHei']
plt.rcParams['axes.unicode_minus'] = False
fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(20, 8), dpi=100)
plt.subplot(221)
# 绘制二项分布的分布律图像
n=10
M =20
N=50
p=M/N
x1=np.arange(0,n)
y1=st.binom.pmf(x1,n,p)
plt.plot(x1,y1,'k--',label='n={},p={}'.format((n),(p)))
#绘制超几何分布的分布律图像
x2= np.arange(0,n)
y2=st.hypergeom.pmf(x2,N,M,n) 
plt.plot(x2,y2,'b',label='n={},N={},M={}'.format((n),(N),(M)))
plt.title('图a 二项分布和超几何分布的近似')
plt.legend()
plt.grid()
plt.subplot(222)
# 绘制二项分布的分布律图像
n=10
M =20
N=60
p=M/N
x1=np.arange(0,n)
y1=st.binom.pmf(x1,n,p)
plt.plot(x1,y1,'k--',label='n={},p={}'.format((n),(p)))
#绘制超几何分布的分布律图像
x2= np.arange(0,n)
y2=st.hypergeom.pmf(x2,N,M,n)
plt.plot(x2,y2,'b',label='n={},N={},M={}'.format((n),(N),(M)))
plt.title('图b 二项分布和超几何分布的近似')
plt.legend()
plt.grid()
plt.subplot(223)
# 绘制二项分布的分布律图像
n=10
M =20
N=100
p=M/N
x1=np.arange(0,n)
y1=st.binom.pmf(x1,n,p)
plt.plot(x1,y1,'k--',label='n={},p={}'.format((n),(p)))
#绘制超几何分布的分布律图像
x2= np.arange(0,n)
y2=st.hypergeom.pmf(x2,N,M,n)
plt.plot(x2,y2,'b',label='n={},N={},M={}'.format((n),(N),(M)))
plt.title('图c 二项分布和超几何分布的近似')
plt.legend()
plt.grid()
plt.subplot(224)
# 绘制二项分布的分布律图像
n=10
M =20
N=1000
p=M/N
x1=np.arange(0,n)
y1=st.binom.pmf(x1,n,p)
plt.plot(x1,y1,'k--',label='n={},p={}'.format((n),(p)))
#绘制超几何分布的分布律图像
x2= np.arange(0,n)
y2 =st.hypergeom.pmf(x2,N,M,n)
plt.plot(x2,y2,'b',label='n={},N={},M={}'.format((n),(N),(M)))
plt.title('图d 二项分布和超几何分布的近似')
plt.legend()
plt.grid()
plt.show() 
