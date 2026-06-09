import numpy as np
import scipy.stats as st
#实际频数值
x=np.array([8,16,17,10,6,2,1,0]) 
#卡方拟合优度检验
def kafangtest(alpha): 
    p=np.array([0,1,2,3,4,5,6,7])    
    n=len(x)
    #总的试验次数
    s=np.sum(x) 
    y=[]
    z=[]
    p1=[]
    s1=0
    s2=0
    #使用极大似然估计法计算样本均值
    for i in range(0,n):
        k=p[i]*x[i]/s   
        s1+=k 
    #修改p中的元素，均乘以n，变为npi    
    for k in p:
        k1=st.poisson.pmf(k,s1)
        #计算pi
        p1.append(k1)
    for i in range(0,n):
        #计算npi
        p1[i]=p1[i]*s   
    for i in p1:
        if i<5: 
            #需要合并的组数
           s2+=1  
    #print(s2) 
    for i in range(0,n):
        y=x-p1
        z=(y**2)/p1
    #统计量的值
    kafang=sum(z) 
    #1-α分位数
    k_percentile1=st.chi2.ppf(1-alpha,n-s2-2) 
    print('统计量的值为',kafang,'卡方分布的分位数为',k_percentile1) 
    #根据拒绝域判断
    if(kafang<k_percentile1 ): 
        print('接受原假设')
    else:
        print('拒绝原假设')
    #利用p值进行检验
    #检验的p值
    p=1-st.chi2.cdf(kafang,n-s2-2) 
    print('检验的p值为',p)   
    #根据p值判断          
    if(p>alpha): 
      print('接受原假设')
    else:
      print('拒绝原假设')      
kafangtest(0.05)