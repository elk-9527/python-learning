import scipy.stats as st
m=10
n=10
#两个总体F检验
def Ftest(alpha):        
    meanx=28
    meany=26
    sx2=35.8
    sy2=32.3
    #使用公式
    c=sx2/sy2 
    #利用分位数进行检验
    #α/2分位数
    k_percentile1=st.f.ppf(1-alpha/2,m-1,n-1)
    #1-α/2分位数
    k_percentile2=st.f.ppf(alpha/2,m-1,n-1) 
    print('统计量的值为',c,'F方分布的分位数为',k_percentile1,k_percentile2) 
    #根据拒绝域判断
    if(k_percentile2<c<k_percentile1): 
      print('接受原假设')
    else:
      print('拒绝原假设')
    #利用p值进行检验
    p=2*(min(1-st.f.cdf(c,m-1,n-1),st.f.cdf(c,m-1,n-1)))
    print('检验的p值为',p)  
#根据p值判断           
    if(p>alpha): 
      print('接受原假设')
    else:
      print('拒绝原假设')    
a=Ftest(0.05)


