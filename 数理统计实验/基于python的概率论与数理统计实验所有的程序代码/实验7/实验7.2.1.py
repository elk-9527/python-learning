import random
#总的实验次数
N=5000 
#总人数
m=10 
#总的楼层数
n=7 
#在某层不停的概率
p=(1-1/n)**m 
#在某层停的概率
q=1-p 
#计算数学期望的理论值
EX=n*q 
#电梯停的层数
count=0 
x=[]
for i in range(1,N+1):
    #将每层电梯的状态置0
    for j in range(1,n):
        x.insert(j,0)  
    for k in range(1,m+1) :
    #电梯在第j层停下，将j赋值为1
        j=random.randint(1, n)
        #将列表x的第j个元素赋值为1
        x.insert(j,1)  
    #如果列表x的第j个元素为1，说明电梯停了一次
    for j in range(1,n+1): 
        if x[j]==1:
            count+=1
#在N次模拟实验中电梯停的平均次数
frequency=count/N 
#计算相对误差
error=abs(EX-frequency)/EX 
print('期望的理论值为',EX,'期望的模拟值为',frequency,'误差为',error)
