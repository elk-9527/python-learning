import scipy.stats as st
import numpy as np
data= [914,920,910,934,953,945,912,924,940]
n=len(data)
mu0=950
def onettestleft(alpha):
    t_percentile=st.t.ppf(alpha,n-1)    
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
      s2=s2+(k-mean)**2
    std=np.sqrt(s2/(n-1))       
    t= (mean-mu0 )/(std/np.sqrt(n))
    print('统计量t值为',t,'t分位数为',t_percentile,'标准差为',std,'均值为',mean)   
    if(t>t_percentile):
      print('接受原假设')
    else:
      print('拒绝原假设')
    #利用p值进行检验
    p=st.t.cdf(t,n-1) 
    print('检验的p值为',p)             
    if(p>alpha): 
        print('接受原假设')
    else:
        print('拒绝原假设')
a=onettestleft(0.05)

