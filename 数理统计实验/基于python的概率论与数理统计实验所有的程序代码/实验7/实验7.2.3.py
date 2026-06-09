import random
import numpy as np
N =10000
n=10
k=6
#将每次随机出现的数字放入列表
X = []  
#计算取了k次后号码的和s
def count():
    s=0
    for i in range(1,k+1):    
        #产生1-n之间的一个随机数
        y = random.randint(1, n)
        #计算取了k次后号码的和s
        s+=y
        #取了k次号码后的号码放在X中
        X.append(y)
    return s    
X1=[]
for i in range(1,N+1):
    #计算取了k次后号码的和s
    b=count() 
    #X1中放了N次重复试验中出现的所有的号码和
    X1.append(b)
    
# 统计X1中每个数字出现的次数，放在c中，不同的元素放在X2中，计算期望的模拟值  
X2 = []  
m=0
c=0
a=[]
d=0
for j in X1:
    if j not in X2:
        X2.append(j)
        
        m+=1
        c=X1.count(j)
        #计算j出现的频率
        c=c/N 
        #计算j*j出现的频率
        c=c*j
        #求和，模拟期望值
        d=d+c
#理论期望值        
p=k*(n+1)/2
print('频率值为',d,'理论值为',p,'误差为',np.abs(d-p)/p) 

