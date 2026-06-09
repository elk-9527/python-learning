import numpy as np
import scipy.stats as st
x=np.array([[550,61],[681,144]])
r=x.shape[0]
s=x.shape[1]
#独立性检验
def kafangtest(alpha): 
    #总的实验次数
    n=np.sum(x) 
    p=[]
    n1=[]
    n2=[]
    #对频数按行求和
    n1=np.sum(x,axis=1) 
    #对频数按列求和
    n2=np.sum(x,axis=0) 
    for i in range(0,r):
        for j in range(0,s):
            k1=n1[i]*n2[j]/n
            k2=(x[i,j]-k1)**2/k1
            p.append(k2)  
    #计算统计量的值       
    kafang=np.sum(p) 
    #1-α分位数
    k_percentile1=st.chi2.ppf(1-alpha,(r-1)*(s-1)) 
    print('统计量的值为',kafang,'卡方分布的分位数为',k_percentile1) 
    #根据拒绝域判断
    if(kafang<k_percentile1 ): 
        print('接受原假设')
    else:
        print('拒绝原假设')
    #利用p值进行检验
    #检验的p值
    p=1-st.chi2.cdf(kafang,(r-1)*(s-1)) 
    print('检验的p值为',p)  
    #根据p值判断           
    if(p>alpha): 
      print('接受原假设')
    else:
      print('拒绝原假设')   
kafangtest(0.05)
