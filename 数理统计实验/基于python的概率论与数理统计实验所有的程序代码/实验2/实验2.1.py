import numpy as np
#掷一枚骰子n次
def onedice(n):
    k=0
    for i in range(1,n+1):
        #模拟一次掷骰子的结果,即出现1到6
        dot=np.random.randint(1, 7)
        if dot==6:
            k=1
    return k
#实验次数，将4次掷骰子实验模拟10000次
N=10000
#s1表示是否出现6点
s1=0 
for i in range(1,N+1):         
    s1+=onedice(4)
f1=s1/N
# 这是模拟得到的频率结果
print(f1)   
#手算的理论值
print(1-(5/6)**4) 

