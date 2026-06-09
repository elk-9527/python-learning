import numpy as np
import scipy.stats as st
x=np.array([23,26,21,20,15,15])
#卡方拟合优度检验
def kafangtest(alpha): 
    p=np.array([1/6,1/6,1/6,1/6,1/6,1/6])    
    n=len(x)
    #总的实验次数
    s=np.sum(x) 
    y=[]
    z=[]
    #修改p中的元素，均乘以n，变为npi
    for i in range(0,n):
        #计算npi
        p[i]=p[i]*s    
        for i in range(0,n+1):
            y=x-p
            z=y**2/p
     #统计量的值
    kafang=np.sum(z) 
    #1-α分位数
    k_percentile1=st.chi2.ppf(1-alpha,n-1) 
    print('统计量的值为',kafang,'卡方分布的分位数为',k_percentile1) 
    #根据拒绝域判断
    if(kafang<k_percentile1 ): 
        print('接受原假设')
    else:
        print('拒绝原假设')
    #利用p值进行检验
    #检验的p值
    p=1-st.chi2.cdf(kafang,n-1) 
    print('检验的p值为',p)  
    #根据p值判断           
    if(p>alpha): 
      print('接受原假设')
    else:
      print('拒绝原假设')  
kafangtest(0.05)
