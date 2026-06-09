import random
import math
#总的实验次数
N=50000 
#信的总数
n=10 
number=0
x={}
#将第i封信配对第i个信封
for i in range(1,n+1): 
    x[i]=i
#交换值   
#利用随机选取产生随机排列
def exchange(x): 
    k=n
    for j in range(1,k+1):
        temp=0  
        s=random.randint(1, k)
        temp=x[s]
        x[s]=x[k]
        x[k]=temp
        k-=1
    return x
#计算配对数
def compute(x): 
    k=0
    for j in range(1,n+1):
        if x[j]==j:
            k+=1
    return k
#计算m阶乘的倒数
def compute1(m): 
    k=1
    #计算阶乘
    for j in range(1,m+1): 
        k=k*j
    k=1/k
    return k
#主程序：
s=0
for i in range(1,N+1):
     y=exchange(x)
     k=compute(y)
     #统计配对的数目
     number+=k 
     #统计至少有一个配对的次数
     if k>=1: 
         s+=1
#模拟的期望值
EX=number/N 
#至少有一个配对的频率
frequency=s/N 
#至少有一个配对的理论概率
sum=0
for i in range(1,n+1):
    if(i%2==1):
        sum+=compute1(i)
    else:
        sum-=compute1(i)
probility=sum
print('（1）至少一个信装对的模拟频率值',frequency, '至少一个信装对的真实概率值为',probility,'至少一个信装对的真实的概率的极限值',1-math.exp(-1),'（2）期望的真实值为',1,'期望模拟的值',EX)

