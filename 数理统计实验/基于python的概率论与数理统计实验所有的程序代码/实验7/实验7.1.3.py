import sympy
# 使用符号变量的时候，需要先导入符号
from sympy.abc import x  
y1=(5-x)/60
y2=(25-x)/60
y3=(55-x)/60
y4=(65-x)/60
EX1=sympy.integrate(y1,(x,0,5))
EX2=sympy.integrate(y2,(x,5,25))
EX3=sympy.integrate(y3,(x,25,55))
EX4=sympy.integrate(y4,(x,55,60))
EX=EX1+EX2+EX3+EX4
print('X的期望为',EX)

