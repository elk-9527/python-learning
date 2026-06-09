import numpy as np
X=np.array([0,1,2])
Y=np.array([0,1,2]) 
p=np.array([[1/15,4/15,1/15],[4/15,4/15,0],[1/15,0,0]])
p1=np.array([1/15,4/15,1/15,4/15,4/15,0,1/15,0,0])
p2=[]
p3=[]
Z=[]
#求分布律
for i in range(3):
    s=0
    for j in range(3):
        s+=p[i][j]
    p2.append(s)
for j in range(3):
    t=0
    for i in range(3):
        t+=p[i][j]
    p3.append(t)
#求X和Y的期望
EX=np.sum(X*p2)
EY=np.sum(Y*p3)
EX2=np.sum(X**2*p2)
EY2=np.sum(Y**2*p3)
DX=EX2-EX**2
DY=EY2-EY**2
print('X的期望为',EX,'Y的期望为',EY,'X 的方差为',DX,'Y的方差为',DY)
#求E(XY)
for j in range(3):
    for i in range(3):
        m= X[i]*Y[j]
        Z.append(m)
EZ=np.sum(Z*p1)        
#计算协方差和相关系数
Cov=EZ-EX*EY
r=Cov/np.sqrt(DX*DY)
print('相关系数为',r)

