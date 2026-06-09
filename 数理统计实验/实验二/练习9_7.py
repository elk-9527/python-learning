import scipy.stats as st
import numpy as np

# 轮胎行驶里程数据（单位：km）
data = [41250, 40187, 43175, 41010, 39265, 41872, 42654, 41287,
        38970, 40200, 42550, 41095, 40680, 43500, 39775, 40400]

def t_mean_interval_bound(confidence):
    alpha=1-confidence
    n=len(data)
    z_percentile=st.norm.ppf(1-alpha)
    t_percentile=st.t.ppf(1-alpha,n-1)
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
    #方差未知，求mu的置信区间，n>30
    if n>=30:
      # 当n>=30时，t分布近似正态分布，使用正态分布的置信区间公式
      lower_limit=mean-z_percentile*std/np.sqrt(n)
    return(lower_limit)
a=t_mean_interval_bound(confidence=0.95)
print('置信下限为',a)

