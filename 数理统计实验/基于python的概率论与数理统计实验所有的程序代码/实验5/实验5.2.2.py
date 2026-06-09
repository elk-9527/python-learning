from scipy.stats import binom
import numpy as np
N=2500
p=0.002
number=12
pay=2000
#保险公司收到的金额
total=number*N 
#赔付最大承受人数
X1=int(total/pay) 
#保险公司赔本的概率
p1=1-binom.cdf(X1,N,p) 
#一年内死亡的人数
puples=np.random.binomial(N,p) 
#赔付金
Pays=pay*puples 
#利润
profits=total-Pays  
print(p1,profits,X1)


