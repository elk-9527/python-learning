import numpy as np
import matplotlib.pyplot as plt
mu=1
sigma=2
count1=0
count2=0
count3=0
x = np.arange(-8,8,0.01)
a = ((x - mu) ** 2) / (2 * (sigma ** 2))
#计算正态分布的密度函数
y = 1 / (sigma * np.sqrt(2 * np.pi)) * np.exp(-a) 
#画图
plt.plot(x, y, color='cyan', label=r'$\mu=%.2f,\ \sigma=%.2f$' % (mu,sigma))
#画出密度函数图像
# 绘制基准水平直线
plt.plot((x.min(),x.max()), (0,0))
# 设置坐标轴标签
plt.xlabel('x')
plt.ylabel('y')
# 填充指定区域，当X 取值落入mu-sigma,mu+sigma区间时用紫色填充
plt.fill_between(x,y, where=(mu-sigma<x) & (x<mu+sigma), facecolor='purple')
# 可以填充多次，当X <mu-sigma或>mu+sigma区间时用绿色填充
#当X <mu-2sigma或>mu+2sigma区间时用蓝色填充
#当X <mu-3sigma或>mu+3sigma区间时用白色填充
plt.fill_between(x,0,y, where=(x<mu-sigma) | (x>mu+sigma),facecolor='green')
plt.fill_between(x,0,y, where=(x<mu-2*sigma) | (x>mu+2*sigma),facecolor='blue')
plt.fill_between(x,0,y, where=(x<mu-3*sigma) | (x>mu+3*sigma),facecolor='white')
plt.show()
#计算频率
N=10000
z=[]
for i in range(N):
    #产生N个服从正态分布的随机数
    k= np.random.normal(mu,sigma) 
    z.append(k)
    if mu-sigma<z[i]<mu+sigma:
        count1+=1
    if mu-2*sigma<z[i]<mu+2*sigma:
        count2+=1
    if mu-3*sigma<z[i]<mu+3*sigma:
        count3+=1
print(count1/N,count2/N,count3/N)

