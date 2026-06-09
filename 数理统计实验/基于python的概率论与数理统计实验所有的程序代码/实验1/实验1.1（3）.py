import matplotlib.pyplot as plt
import random
#返回0或者1
def r():
    s=random.randint(0,1)
    return s
times=5000
indices=[]
#储存朝上的频率
f = []
for i in range(1,times+1):
    #做i次实验正面向上事件次数
    heads = 0  
    for j in range(i):
        if r() == 1:
            heads+=1
    f.append(heads/i)
    indices.append(i)
print(heads/times)
plt.plot(indices,f)
plt.show()

