import numpy as np
import scipy.stats as st
alpha = 0.05
data= [6,8,4,6,-3,7,2,6,-2,-1]
mu0=0
n= len(data)
m=np.mean(data)
s=np.std(data, ddof = 1)
t,p_two1 = st.ttest_1samp(data,mu0)
#手动计算c值
c= (m- mu0)*np.sqrt(n)/s 
print('t值=',t,'包中的双尾检验的P值',p_two1)
if(p_two1 < alpha):
    print('拒绝原假设')
else:
    print('接受原假设')
#手动计算p值
p1=2-2*st.t.cdf(abs(t),n-1) 
print('手动计算p值=',p1,'手动计算t值=',c)

