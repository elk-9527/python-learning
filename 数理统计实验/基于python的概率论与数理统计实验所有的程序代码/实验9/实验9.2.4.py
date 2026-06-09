import scipy.stats as st
data=[7.5,2,12.1,8.8,9.4,7.3,1.9,2.8,7,7.3]
#求方差的置信区间
def onekafanginterval(mu,confidence):
    alpha=1-confidence
    n=len(data)
    kf_percentile1=st.chi2.ppf(1-alpha/2,n-1)
    kf_percentile2=st.chi2.ppf(alpha/2,n-1)
    kf_percentile3=st.chi2.ppf(1-alpha/2,n)
    kf_percentile4=st.chi2.ppf(alpha/2,n)
    s1=0
    s2=0
    s3=0
    #期望未知，求方差的置信区间，n<30
    if n<30 and mu==None:
        #计算均值
        for i in range(0,n):
            k=data[i]
            s1=s1+k 
        mean=s1/n 
        #计算样本方差
        for i in range(0,n):
           k=data[i]
           s2=s2+(k-mean)**2   
        lower=s2/kf_percentile1
        upper=s2/kf_percentile2
    #期望未知，求方差的置信区间，n<30
    if n<30 and mu!=None:
         for i in range(0,n):
            k=data[i]
            s3=s3+(k-mu)**2  
         lower=s3/kf_percentile3
         upper=s3/kf_percentile4
    return(lower,upper)
b=onekafanginterval(6.5,0.95)
print('置信区间为',b)

