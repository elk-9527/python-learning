import numpy as np
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
#生成x步长为0.1的列表数据
x = np.arange(-8,8,0.1)
#生成y1
u=[1,2,4]
s=[1,np.sqrt(2),2]
for i in u:
    a =((x - i) ** 2) / (2 * (s[0] ** 2))
    y =( 1 / (s[0] * np.sqrt(2 * np.pi))) * np.exp(-a) 
    plt.plot(x, y, label=r'$\mu=%.2f,\ \sigma^2=%.2f$' % (i,s[0]**2))
for j in s:
    a1 =((x - u[1]) ** 2) / (2 * (j ** 2))
    y1 =( 1 / (j * np.sqrt(2 * np.pi))) * np.exp(-a1)
    plt.plot(x, y1, label=r'$\mu=%.2f,\ \sigma^2=%.2f$' % (u[1],j**2))
#调整标签的大小和位置
plt.legend(loc='upper left',fontsize=10) 
plt.show()


