import scipy.stats as st
import numpy as np
data1=[628,583,510,554,612,523,530,615]
data2=[535,433,398,470,567,480,498,560,503,426]
#当总体方差未知但是相等时，求mu1-mu2的置信区间
def twomean_t_interval(confidence):
    alpha=1-confidence
    n1=len(data1)
    n2=len(data2)
    z_percentile=st.norm.ppf(1-alpha/2)
    t_percentile=st.t.ppf(1-alpha/2,n1+n2-2)
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
    #计算样本方差
    s3=0
    s4=0
    for i in range(0,n1):
      k=data1[i]
      s3=s3+(k-mean1)**2
    for i in range(0,n2):
      k=data2[i]
      s4=s4+(k-mean2)**2
    sw=np.sqrt((s3+s4)/(n1+n2-2))
    #print(mean1,mean2,s3/(n1-1),s4/(n2-1),sw) 
    #方差已知，求mu1-mu2的置信区间
    if n1<30 and n2<30:
      lower_limit = mean1 - mean2 - t_percentile*sw*np.sqrt(1/n1+1/n2)
      upper_limit = mean1 - mean2 + t_percentile*sw*np.sqrt(1/n1+1/n2)
    #方差未知，求mu1-mu2的置信区间 ,n>30
    if n1>30 or n2>30: 
      lower_limit = mean1 - mean2 - z_percentile*np.sqrt(s3/n1+s4/n2)
      upper_limit = mean1 - mean2 + z_percentile*np.sqrt(s3/n1+s4/n2)
    return(lower_limit, upper_limit)
b=twomean_t_interval(0.95)
print('置信区间为',b)
