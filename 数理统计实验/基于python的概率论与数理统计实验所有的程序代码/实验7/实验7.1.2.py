import sympy
# 使用符号变量的时候，需要先导入符号
from sympy.abc import x  
y=sympy.exp(-2*x)*x*2#
EX=sympy.integrate(y,(x,0,float('inf')))
y1=sympy.exp(-2*x)*(x-EX)**2*2
y2= sympy.exp(-2*x)*(x**2)*2
y3=sympy.exp(-2*x)*(x**2-1)*2
#直接使用方差的定义求方差
DX=sympy.integrate(y1,(x,0,float('inf'))) 
#求x的平方的期望
EX2=sympy.integrate(y2,(x,0,float('inf'))) 
#使用方差的计算公式求方差
DX1=EX2-EX**2 
#求x平方-1的数学期望
EY=sympy.integrate(y3,(x,0,float('inf'))) 
print('X的期望为',EX,'X的方差为',DX,'X2-1的期望为',EY)

