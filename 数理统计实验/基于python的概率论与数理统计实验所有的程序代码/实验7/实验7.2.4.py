import numpy as np
N =10000
# 将每次随机出现的数字放入列表
X =[] 
#求利润，a表示进货量，b表示需求量
def profit(a,b): 
    if a<=b:
        s=1.5*a
    else:
        s=1.5*b-0.5*(a-b)
    return s
for i in range(0,20):
    X.append(0)
for i in range(1,N+1):
     #需求量
     b=np.random.randint(30,50) 
     #进货
     for a in range(30,50): 
         X[a-30]+=profit(a,b)
#进货
for a in range(0,20): 
    X[a]=X[a]/N
#i表示列表的下标，j表示下标对应的值
for i,j in enumerate(X): 
    a=i+30
    p=j
    print("进货量为",a,"利润为",p)
