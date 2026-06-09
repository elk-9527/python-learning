from scipy.optimize import fsolve
data=[100,130,120,138,110,110,115,134,120,122,110,120,115,162, 130,130,110,
147,122,131,110,138,124,122,126,120,130]
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
#解方程组求解mu,sigma2
#定义方程组
def func(i):
    mu, sigma2= i[0], i[1]
    return [         
            mu-M1,
            sigma2-B2,
           ] 
#解方程组
r = fsolve(func,[5, 0.3]) 
#输出结果并验证
print('样本均值为',M1,'二阶中心矩为',B2,'方程组的解为',r) 


