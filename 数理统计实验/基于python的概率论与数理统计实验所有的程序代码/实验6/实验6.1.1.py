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
#设置x、y轴上刻度显示方向
ax.axis["x"].set_axis_direction("top")
ax.axis["y"].set_axis_direction("right")
#生成步长为0.1的列表数据x
x = np.arange(-8,8,0.1)
#生成y
for s in [(0, 1), (-1, 2), (-2, np.sqrt(0.5))]:
    a, b= s[0], s[1]
    y =st.norm.cdf(x,a,b) 
    plt.plot(x, y, label=r'$\mu=%.2f,\ \sigma^2=%.2f$' % (a,b**2))
#调整标签的大小和位置
plt.legend(loc='upper left',fontsize=10) 
plt.show()   

