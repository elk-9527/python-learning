import numpy as np
N=50000 
#旧球数为6
old=6  
#新球数为9
new=9  
#总的球数
total=old+new 
#定义函数，模拟一次实验
def pingpangqiu():
    #第一次取出几个新球
    s1=0  
    #第二次取出几个新球
    s2=0  
    k=0
    #定义函数ball，用来将列表X1的前6个元素标记为0，表示6个旧球；后9个元素标记为1，表示9个新球。
    def ball():
    #表示球的新旧情况
        x1=[] 
        for i in range(1,total+1):
            if i<=old:
                k=0
            else:
                k=1
            x1.append(k)
        return(x1)
    #调用函数ball，得到y1为球的新旧情况。
    y1=ball()        
    #第一次取球        
    for i in range(3):
            #从1到总的球数total-i+1中取一个随机数
            k=np.random.randint(1,total-i+1) 
            #如果取得的球是新球，则s1+1；若取得的是旧球，则s1不变。
            if y1[k-1]==1: 
               s1+=1
            else:
               s1+=0
             #取出的球不再放回，删掉
            del y1[k-1]	
    #第二次取球
    #因为第一次取出的新球再次放回已经变成了旧球，故定义函数ball1，用来将列表x2的前6+s1个元素标记为0，表示6+s1个旧球；后9-s1个元素标记为1，表示9-s1个新球。
    def ball1():
        #表示球的新旧情况
        x2=[] 
        #s1表示第一次取出的新球的数目
        for i in range(1,total+1): 
            if i<=old+s1:
                k=0
            else:
                k=1
            x2.append(k)
        return(x2)
    y2=ball1()     
    for i in range(3): 
        k=np.random.randint(1,total-i+1) 
        #如果取得是新球，s2+1；否则s2不变。
        if y2[k-1]==1: 
              s2+=1
        else:
              s2+=0
        del y2[k-1]
    #函数返回的结果为s1,s2，即第一次和第二次的取出的新球数
    return(s1,s2) 
#接收s1,s2
z=[]
#两次取得都是新球
number1=0 
#第二次取得是新球
number2=0 
#把上述程序重复运行N次，计算频率
for i in range(N):
    z=pingpangqiu()
    #如果第二次取的3个新球
    if z[1]==3: 
        number2+=1
    #如果两次取得都是3个新球，则number1+1
    if z[0]==3 and z[1]==3:
        number1+=1  
#第二次取得全是新球的频率
f1=number2/N 
#在第二次取得全是新球的条件下，第一次取得全是新球的频率
f2=number1/number2 
print(f1,f2)

