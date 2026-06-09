import numpy as np
import scipy.stats as st
from matplotlib import pyplot as plt
import mpl_toolkits.axisartist as axisartist
#创建画布
fig = plt.figure(figsize=(8, 8))
#使用axisartist.Subplot方法创建一个绘图区对象ax
ax = axisartist.Subplot(fig, 111)  
#将绘图区对象添加到画布中
fig.add_axes(ax)
#通过set_visible方法设置绘图区所有坐标轴隐藏
ax.axis[:].set_visible(False)
#ax.new_floating_axis代表添加新的坐标轴
ax.axis["x"] = ax.new_floating_axis(0,0)
#给x轴加上箭头
ax.axis["x"].set_axisline_style("->", size = 1.0)
#添加y轴，并加上箭头
ax.axis["y"] = ax.new_floating_axis(1,0)
ax.axis["y"].set_axisline_style("-|>", size = 1.0)
#设置x轴、y轴上刻度显示方向
ax.axis["x"].set_axis_direction("top")
ax.axis["y"].set_axis_direction("right")
#生成步长为0.1的列表数据x
x = np.arange(-8,8,0.1)
#生成y1
u=[1,2,4]
s=[1,np.sqrt(2),2]
for i in u:
    y =st.norm.pdf(x,i,s[0]) 
    plt.plot(x, y, label=r'$\mu1=%.2f,\ \sigma^2=%.2f$' % (i,s[0]**2))
for j in s:
    y1=st.norm.pdf(x,u[1],j) 
    plt.plot(x, y1, label=r'$\mu=%.2f,\ \sigma^2=%.2f$' % (u[1],j**2))
#调整标签的大小和位置
plt.legend(loc='upper left',fontsize=10) 
plt.show()

