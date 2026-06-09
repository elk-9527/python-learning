import numpy as np
import sympy
data=[1,2,1,1,5,1]
#将λ符号化
lamb=sympy.symbols('lamb',positive=True) 
l=len(data)
X=[]
#计算阶乘，定义阶乘函数为factorial
def factorial(n):
    s=1
    for k in range (1,n+1):
        s=s*k
    return s
for i in range(0,l):
  k=data[i]
  #分布律或密度函数
  f=lamb**(k)*np.e**(-lamb)/factorial(k) 
  X.append(f)  
#似然函数,#np.prod()函数用来计算所有元素的乘积，对于有多个维度的数组可以指定轴，如axis=1指定计算每一行的乘积。变量替换subs函数，用i替换x
L=np.prod(X)
print('似然函数为',L)
#取对数
lnL=sympy.expand_log(sympy.log(L)) 
print('对数似然函数为',lnL)
diff=sympy.diff(lnL,lamb)
print('微分方程为',diff)
#solve()函数解方程,diff()函数计算微分,diff(func,var,n)计算高阶微分
solve=sympy.solve(diff) 
print('解为',solve,'均值为',np.mean(data))


