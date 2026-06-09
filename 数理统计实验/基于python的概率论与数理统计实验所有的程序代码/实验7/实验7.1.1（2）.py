import numpy as np
X=np.array([-2,-1,0,1,2] )
p=np.array([0.3,0.1,0.2,0.1,0.3]) 
EX=sum(X*p)
EX2=sum(X**2*p)
DX=EX2-EX**2
Y=X**2-1
EY=sum(Y*p)
EY2=sum(Y**2*p)
DY=EY2-EY**2
print('X的期望为',EX,'X的方差为',DX,'Y的期望为',EY,'Y的方差为',DY)


