import sympy 
# 使用符号变量的时候，需要先导入符号，定义θ为符号
from sympy.abc import theta 
#给出样本观测值
data=[0.1,0.4,0.5,0.3,0.2] 
#样本容量
l=len(data) 
#计算样本均值
s1=0
for i in range(0,l):
    k=data[i]
    s1=s1+k
M1=s1/l
print('均值为',M1)
#解方程：M1=（θ+1）/（θ+2），求出θ
r = sympy.solve((theta+1)/(theta+2)-M1,theta)
print('方程的解为',r,(2*M1-1)/(1-M1))

