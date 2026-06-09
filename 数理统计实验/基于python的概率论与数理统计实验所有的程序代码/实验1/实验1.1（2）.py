import matplotlib.pyplot as plt
import random
times = 10000
# 将每次随机出现的数字放入列表
count = []  
for i in range(1, times+1):
    y = random.randint(0, 1)
    count.append(y)
#统计0和1出现的次数，计算频率，1表示正面向上    
s1=0
s2= 0
for k in count:
    if k ==0:
        s1+= 1
    else:
        s2+=1
f1=s2
print(f1/times)
#画图展示每次试验正面向上出现的频率
#储存朝上的频率
f = []  
indices=[]
#i表示做的试验次数
for i in range(1,times+1): 
    #做i次实验正面向上事件的次数
    heads = 0 
    for j in range(i):
        if count[j]==1:
            heads+=1
    #计算频率
    f.append(heads/i) 
    #第i次试验
    indices.append(i) 
plt.plot(indices,f)
plt.show()

