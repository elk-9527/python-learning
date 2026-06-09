#导入解方程组的包
from scipy.optimize import fsolve 
data=[1,2,2,3,5,3,4,5,6]
l=len(data)
#计算样本均值
s1=0
s2=0
for i in range(0,l):
    k=data[i]
    s1=s1+k
M1=s1/l
#计算样本二阶中心矩
for i in range(0,l):
    k=data[i]
    s2=s2+(k-M1)**2
B2=s2/l 
#解方程组求解m,p
#定义方程组
def func(i):
    m, p = i[0], i[1]
    return [         
            m*p-M1,
            m*p-m*p**2-B2,
           ]
#解方程组
r = fsolve(func,[19, 0.3])
print('一阶原点矩=',M1,'二阶中心矩=',B2,'解=',r)
#验证结果
print('理论分析的计算结果为',M1**2/(M1-B2),1-B2/M1) 
