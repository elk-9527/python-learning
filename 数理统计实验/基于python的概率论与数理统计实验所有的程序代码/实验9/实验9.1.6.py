import numpy as np
import sympy
m=20
data=[1,2,4,2,3,5,6,8]
l=len(data)
X=[]
#将p符号化
p=sympy.symbols('p',positive=True) 
def factorial(n):
    s=1
    for i in range(1,n+1):
        s=s*i
    return s
#计算组合数
def combinateC(n,m):
    c=factorial(n)/(factorial(m)*factorial(n-m))
    return c
for i in range(0,l):
    k=data[i]
    #分布律或密度函数
    f=combinateC(m,k)*(p**k)*((1-p)**(m-k)) 
    X.append(f)  
#似然函数,np.prod()函数用来计算所有元素的乘积
L=np.prod([X]) 
print('似然函数为',L)
#取对数
lnL=sympy.expand_log(sympy.log(L)) 
print('对数似然函数为',lnL)
diff=sympy.diff(lnL,p)
print('微分方程为',diff)
#solve()函数解方程,diff()函数计算微分,diff(func,var,n)计算高阶微分
solve=sympy.solve(diff) 
print('解为',solve,'均值为',np.mean(data)/m)

