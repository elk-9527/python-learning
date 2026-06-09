import random
from scipy.stats import binom
#用中心极限定理计算机床台数
N =1000
M=200
p=0.6
X=[]
# 将每次随机出现的数字放入列表
Y=[] 
#统计小于概率p的概率的数目，这是能正常的工作的机器数
def bimachine():
    s=0
    for i in range(1,M+1):    
        #产生1000个0-1之间的一个随机数
        y = random.random()
        if y<p:
            #计算正常的机器数目
            s+=1 
    return s    
for i in range(1,N+1):
    a=bimachine()
    X.append(a)
#对X进行排序
Y=sorted(X) 
#输出倒数第二个
print(Y[N-1]) 
#使用二项分布计算正常工作的车床的台数 
n = 200
p = 0.6
#ppf:累积分布函数的反函数。q=0.01时，ppf就是p(X<x)=0.01时的x值。
#计算当n=200,p=0.2时，概率大于等于0.999的数目
print(binom.ppf(0.999,n,p)) 
print(binom.cdf(141,n,p))
