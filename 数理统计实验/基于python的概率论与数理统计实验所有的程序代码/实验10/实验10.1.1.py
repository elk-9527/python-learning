# stats模块是scipy库中的一个模块，用于显著性检验
import scipy.stats as st
import numpy as np
data=[19.8,20.3,20.4,19.9,20.2,19.6,20.5,20.1]
n=len(data)
mu0=20
#单个样本Z检验，使用公式
def oneztest(sigma,alpha):        
    #计算均值
    s1=0
    for i in range(0,n):
      k=data[i]
      s1=s1+k 
    mean=s1/n
    #使用公式计算统计量的值
    z= (mean-mu0 )/(sigma/np.sqrt(n)) 
    #利用分位数进行检验
    z_percentile=st.norm.ppf(1-alpha/2)#Z1-α/2
    print('统计量的值为',z,'标准正态分布的分位数为',z_percentile,'均值为',mean) 
    #根据拒绝域判断
    if(abs(z)<z_percentile): 
      print('接受原假设')
    else:
      print('拒绝原假设')
    #利用p值进行检验
    p=2*(1-st.norm.cdf(abs(z))) 
    print('检验的p值为',p) 
    #根据p值判断           
    if(p>alpha): 
      print('接受原假设')
    else:
      print('拒绝原假设') 
a=oneztest(np.sqrt(0.05),0.05)


