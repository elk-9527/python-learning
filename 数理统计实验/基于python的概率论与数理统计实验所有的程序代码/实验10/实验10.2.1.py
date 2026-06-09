import scipy.stats as st
import numpy as np
m=50
n=50
mu=0
#两个样本Z检验，使用公式
def twoztest(sigma1,sigma2,alpha):        
    meanx=1000
    meany=1010
    #使用公式计算统计量的值
    z= (meanx-meany )/np.sqrt((sigma1**2)/m+(sigma2**2)/n) 
    #利用分位数进行检验
    z_percentile=st.norm.ppf(1-alpha/2)
    print('统计量的值为',z,'标准正态分布的分位数为',z_percentile) 
    #根据拒绝域判断
    if(abs(z)<z_percentile): 
      print('接受原假设')
    else:
      print('拒绝原假设')
    #利用p值进行检验
    #检验的p值
    p=2*(1-st.norm.cdf(abs(z))) 
    print('检验的p值为',p)  
    #根据p值判断           
    if(p>alpha): 
      print('接受原假设')
    else:
      print('拒绝原假设') 
a=twoztest(80,90,0.05)


