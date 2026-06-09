import scipy.stats as st
data=[100,110,101,105,95,98,80,114,100]
n=len(data)
mu0=20
#单个总体卡方检验，使用公式
def onekafangtest(mu,sigma,alpha):       
    #计算均值
    s1=0
    for i in range(0,n):
      k1=data[i]
      s1=s1+k1 
    mean=s1/n
    #计算样本方差
    s2=0
    for i in range(0,n):        
        k1=data[i]
        s2=s2+(k1-mu)**2
    #使用公式
    f=s2/(sigma**2) 
    #利用分位数进行检验
    #1-α/2分位数
    k_percentile1=st.chi2.ppf(1-alpha/2,n) 
#α/2分位数
    k_percentile2=st.chi2.ppf(alpha/2,n)    
    print('统计量的值为',f,'卡方分布的分位数为',k_percentile1,k_percentile2) 
    #根据拒绝域判断
    if(k_percentile2<f<k_percentile1 ): 
      print('接受原假设')
    else:
      print('拒绝原假设')
    #利用p值进行检验
    #检验的p值
    p=2*(min(1-st.chi2.cdf(f,n),st.chi2.cdf(f,n))) 
    print('检验的p值为',p)   
    #根据p值判断          
    if(p>alpha): 
      print('接受原假设')
    else:
      print('拒绝原假设')    
a=onekafangtest(100,8,0.05)

