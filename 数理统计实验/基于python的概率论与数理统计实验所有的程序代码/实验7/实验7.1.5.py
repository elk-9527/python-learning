import numpy as np
from scipy.integrate import dblquad
y1=lambda x,y: x*(x+y)/8
y2=lambda x,y: y*(x+y)/8
y3=lambda x,y: (x**2)*(x+y)/8
y4=lambda x,y: (y**2)*(x+y)/8
y5=lambda x,y: x*y*(x+y)/8
EX,error1=dblquad(y1,0,2,lambda g:0,lambda h:2)
EY,error2=dblquad(y2,0,2,lambda g:0,lambda h:2)
EX2,error3=dblquad(y3,0,2,lambda g:0,lambda h:2)
EY2,error4=dblquad(y4,0,2,lambda g:0,lambda h:2)
EXY,error5=dblquad(y5,0,2,lambda g:0,lambda h:2)
DX=EX2-EX**2
DY=EY2-EY**2
Cov=EXY-EX*EY
r=Cov/(np.sqrt(DX*DY))
print('X的期望为',EX,'X的方差为',DX,'Y的期望为',EY,'Y的方差为',DY,'相关系数为',r)

