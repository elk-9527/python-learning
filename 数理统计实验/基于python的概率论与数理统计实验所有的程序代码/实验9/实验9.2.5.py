import scipy.stats as st
import numpy as np
data1=[628,583,510,554,612,523,530,615]
data2=[535,433,398,470,567,480,498,560,503,426]
#当总体方差已知时，求mu1-mu2的置信区间
def twomean_z_interval(sigma1,sigma2,confidence):
    alpha=1-confidence
    n1=len(data1)
    n2=len(data2)
    z_percentile=st.norm.ppf(1-alpha/2)
    #计算均值
    s1=0
    s2=0
    for i in range(0,n1):
      k=data1[i]
      s1=s1+k 
    mean1=s1/n1
    for i in range(0,n2):
      k=data2[i]
      s2=s2+k 
    mean2=s2/n2
    #print(mean1,mean2)     
    #方差已知，求mu的置信区间   
    lower_limit=mean1-mean2-z_percentile*np.sqrt(sigma1**2/n1+sigma2**2/n2)
    upper_limit=mean1-mean2+z_percentile*np.sqrt(sigma1**2/n1+sigma2**2/n2)      
    return(lower_limit,upper_limit)
a=twomean_z_interval(sigma1=0.6,sigma2=1,confidence=0.95)
print('置信区间为',a)

