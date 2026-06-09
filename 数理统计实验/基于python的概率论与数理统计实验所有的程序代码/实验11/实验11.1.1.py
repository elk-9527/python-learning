import numpy as np
import scipy.stats as st
X=np.array([[87.4,85,80.2],[56.2,62.4],[55,48.2],[75.2,72.3,81.3]])
r=X.shape[0]
#求第i个样本的容量
z=[]
for i in range(0,r):
    s=len(X[i])
    z.append(s)
alpha=0.01
#计算组内均值
def mean(x):
    s1=0    
    m=len(x)
    for i in range(0,m):
        k=x[i]
        s1=s1+k 
    s1=s1/m
    return s1
#计算组内和
def sum(x):
    s2=0
    m=len(x)
    for i in range(0,m):
        s2+=x[i]
    return s2
n=sum(z)
#计算总的样本均值
y=[]
for i in range(0,r):
#计算第i个样本均值
    a=sum(X[i]) 
    y.append(a)
b=sum(y)
#计算总的样本均值
b=b/n 
#计算总的偏差平方和  
c=[]
#（xij-均值）的平方求和
def sum1(x): 
    s3=0
    for i in range(0,r):
        for j in range(0,z[i]):
            k=x[i][j]
            s3=s3+(k-b)**2
    return s3
ST=sum1(X)
#计算组内偏差平方和
#（xij-均值）的平方求和
def sum2(x): 
    s4=0
    for i in range(0,r):
       for j in range(0,z[i]):
            k=x[i][j]
            s4=s4+(k-y[i]/z[i])**2
    return s4
SE=sum2(X)
#计算组间偏差平方和
#（xij-均值）的平方求和
def sum3(x): 
    s5=0
    for i in range(0,r):        
        s5+=z[i]*((y[i]/z[i]-b)**2)
    return s5
SA=sum3(X)
#使用F检验给出结论
f=(n-r)*SA/(SE*(r-1))
f_percentile=st.f.ppf(1-alpha,r-1,n-r)
if(f>f_percentile):
    print('拒绝原假设,认为诸因子水平间有显著性差异')
else:
    print('接受原假设')
print('总的离差平方和为',ST,'组内偏差平方和为',SE,'组间偏差平方和为',SA,'F的值为',f)
print('总的样本均值为',b,'第i个水平的样本均值为',y)
