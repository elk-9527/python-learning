import numpy as np
from scipy.stats import t
m=10
n=10
#两个样本t检验
def twottest(alpha):       
    meanx=28
    meany=26
    sx2=35.8
    sy2=32.3
    s=np.sqrt((1/m)+(1/n))
    sw=np.sqrt(((m-1)*sx2+(n-1)*sy2)/(m+n-2))
    #使用公式计算统计量的值
    c= (meanx-meany )/(s*sw) 
    #利用分位数进行检验
    t1=t.ppf(1-alpha/2, df=m+n-2)
    print('t值=',c,'分位数=',t1)
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
a=twottest(0.05)


