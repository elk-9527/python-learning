import numpy as np
import sympy
p=0.5 
data=[0,0,1,1,0,1]
l=len(data)
X=[]
#将p符号化
p=sympy.symbols('p',positive=True) 
for i in range(0,l):
  k=data[i]
  #分布律或密度函数
  f=(p**k)*((1-p)**(1-k)) 
  #X的元素为f(x1), f(x2) ,……,f(xn)
  X.append(f)  
#求似然函数， np.prod()函数用来计算所有元素的乘积，对于有多个维度的数组可以指定轴，如axis=1指定计算每一行的乘积。
L=np.prod([X]) 
print('似然函数为',L)
#取对数
lnL=sympy.expand_log(sympy.log(L)) 
print('对数似然函数为',lnL)
diff=sympy.diff(lnL,p)
print('微分方程为',diff)
#solve()函数解方程,diff()函数计算微分,diff(func,var,n)计算高阶微分
solve=sympy.solve(diff) 
print('解为',solve,'均值为',np.mean(data))

