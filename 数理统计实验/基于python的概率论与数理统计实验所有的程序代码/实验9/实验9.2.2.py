import scipy.stats as st
import numpy as np
data=[60,57,58,65,70,63,56,61,50]
def t_mean_interval(confidence):
    alpha=1-confidence
    n=len(data)
    z_percentile=st.norm.ppf(1-alpha/2)
    t_percentile=st.t.ppf(1-alpha/2,n-1)
    #计算均值
    s1=0
    s2=0
    for i in range(0,n):
      k=data[i]
      s1=s1+k 
    mean=s1/n
    #计算样本方差
    for i in range(0,n):
      k=data[i]
      s2=s2+(k-mean) **2
    std=np.sqrt(s2/(n-1))
    #方差未知，求mu的置信区间，n<30
    if n<30:
      lower_limit=mean-t_percentile*std/np.sqrt(n)
      upper_limit=mean+t_percentile*std/np.sqrt(n)
    #方差未知，求mu的置信区间，n>30
    if n>=30:
      # 当n>=30时，t分布近似正态分布，使用正态分布的置信区间公式
      lower_limit=mean-z_percentile*std/np.sqrt(n)
      upper_limit=mean+z_percentile*std/np.sqrt(n) 
    return(lower_limit,upper_limit)
a=t_mean_interval(confidence=0.95)
print('置信区间为',a)

