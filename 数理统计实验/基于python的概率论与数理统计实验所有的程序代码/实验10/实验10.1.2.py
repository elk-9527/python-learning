import scipy.stats as st
import numpy as np
n=25
mu0=1000
sigma=100
def oneztestleft(alpha):
    z_percentile=-st.norm.ppf(1-alpha)
    mean=950
    z= (mean-mu0 )/(sigma/np.sqrt(n))
    print('统计量的值为',z,'标准正态分布的分位数为',z_percentile,'均值为',mean)  
    if(abs(z)<z_percentile):
      print('接受原假设')
    else:
      print('拒绝原假设')
    #利用p值进行检验
    #检验的p值
    p=st.norm.cdf(z) 
    print('检验的p值为',p)  
    #根据p值判断          
    if(p>alpha): 
      print('接受原假设')
    else:
      print('拒绝原假设') 
a=oneztestleft(0.05)
