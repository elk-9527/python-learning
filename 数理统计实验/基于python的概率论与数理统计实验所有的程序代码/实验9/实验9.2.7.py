import scipy.stats as st
data1=[5.06,5.08,5.03,5.00,5.07]
data2=[4.98,5.03,4.97,4.99,5.02,4.95]
n1=len(data1)
n2=len(data2)
#当总体期望已知时，求方差比的置信区间
def twovariance_interval1(confidence):
    alpha=1-confidence
    F_percentile1=st.f.ppf(1-alpha/2,n1-1,n2-1)
    F_percentile2=st.f.ppf(alpha/2,n1-1,n2-1)    
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
    s3=s3/(n1-1)    
    for i in range(0,n2):
      k=data2[i]
      s4=s4+(k-mean2)**2
    s4=s4/(n2-1)
    #print(s3,s4)     
    #总体的期望未知，求方差比的置信区间
    lower_limit=(s3/s4)*(1/F_percentile1)
    upper_limit=(s3/s4)*(1/F_percentile2)         
    return(lower_limit,upper_limit)    
a=twovariance_interval1(confidence=0.95)
print('置信区间为',a)

