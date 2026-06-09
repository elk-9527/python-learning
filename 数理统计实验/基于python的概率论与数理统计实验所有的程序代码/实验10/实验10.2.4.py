import numpy as np
from scipy.stats import t
x=np.array([148,165,160,171,154,156,142,149,151,160])
y=np.array([104,96,103,103,90,108,119,92,102,100])
z=x-y
n=len(z)
#配对样本t检验
def pairttest(alpha):        
    meanz=np.mean(z)
    sz=np.std(z,ddof=1)
    #使用公式计算统计量的值
    c= meanz*np.sqrt(n)/sz 
    #利用分位数进行检验
    t1=t.ppf(1-alpha/2, df=n-1)
    print('t值=',c,'分位数=',t1,'样本均值',meanz,'样本方差',sz)
    if(abs(c)<t1):
      print('接受原假设')
    else:
      print('拒绝原假设')
    #利用p值进行检验
    #检验的p值
    p=2*(1-t.cdf(abs(c),n-1)) 
    print('检验的p值为',p) 
    #根据p值判断            
    if(p>alpha): 
       print('接受原假设')
    else:
       print('拒绝原假设')
a=pairttest(0.05)

