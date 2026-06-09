import numpy as np
from scipy.stats import poisson
N =20000
l=7
# 将每次随机出现的数字放入列表
X = []  
s=0
for i in range(1,N+1):    
    #产生服从参数λ的N个随机数
    a = np.random.poisson(lam=7,size=None) 
    #将生成的随机数放入列表中
    X.append(a) 
    #对X按照从小到大排序
    Y=sorted(X) 
    n=int(N*0.999)
#找倒数第二个数
print(Y[n]) 
#求题目的理论答案值
print(poisson.ppf(0.999,l)) 

