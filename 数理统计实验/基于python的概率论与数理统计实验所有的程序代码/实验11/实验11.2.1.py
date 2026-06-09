import scipy.stats as st
x=[2.07,3.1,4.14,5.17,6.2]
y=[128,194,273,372,454]
n=len(x)
alpha=0.01
lxx=0
lyy=0
lxy=0
#计算均值
def mean(x):
    s1=0    
    for i in range(0,n):
        k=x[i]
        s1=s1+k 
    s1=s1/n
    return s1    
 #计算样本方差
for i in range(0,n):
    k=x[i]
    lxx=lxx+(k-mean(x))**2          
for i in range(0,n):
    k=y[i]
    lyy=lyy+(k-mean(y))**2
for i in range(0,n):
    k=x[i]*y[i]
    lxy=lxy+k
lxy=lxy-n*mean(x)*mean(y)
#回归方程的系数        
b=lxy/lxx
a=mean(y)-b*mean(x)  
print('常数项为',a,'回归方程的系数为',b,'自变量X的离差平方和为',lxx,'lxy为',lxy,'自变量y的离差平方和为',lyy)
#计算回归平方和和误差平方和，F的值
ST=lyy
SR=b**2*lxx
SE=lyy-SR     
f_percentile=st.f.ppf(1-alpha,1,n-2)
f=(n-2)*SR/SE
print('总的离差平方和为',ST,'误差平方和为',SE,'回归平方和为',SR,'F的值为',f,'F分布的分位数为',f_percentile)   
if(f>f_percentile):
    print('拒绝原假设，回归效果显著')
else:
    print('接受原假设')



