import scipy.stats as st
import numpy as np
data=[6,5.7,5.8,6.5,7,6.3,5.6,6.1,5]
def norm_mean_interval(sigma,confidence):
    alpha=1-confidence
    n=len(data)
    z_percentile=st.norm.ppf(1-alpha/2)
    #计算均值
    s1=0
    for i in range(0,n):
      k=data[i]
      s1=s1+k 
    mean=s1/n
    #方差已知，求mu的置信区间
    lower=mean-z_percentile*sigma/np.sqrt(n)
    upper=mean+z_percentile*sigma/np.sqrt(n)
    return(lower,upper)
a=norm_mean_interval(sigma=1,confidence=0.95)
print('置信区间为',a)
