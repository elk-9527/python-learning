import numpy as np
#总的实验次数
N=10000 
#红球数为8
n1=8  
#黑球数为4
n2=4  
#总的球数
n=n1+n2 
s=0
#定义函数qiu，模拟一次实验
def qiu():
    k=0
    #定义函数ball，用来将列表X1的前8个数标成0，后4个数标称1，表示8个红色球，4个黑色球。
    def ball():
        #表示球的颜色
        x1=[] 
        for i in range(0,n):
            if i<n1:
                k=0
            else:
                k=1
            x1.append(k)
        return(x1)
    #调用函数ball，得到的y1为球的两种颜色的情况
    y1=ball()
    #第一个人取球        
    #从第0号到第n-1号球随机的取一个球
    k=np.random.randint(0,n) 
    #若取得是黑球，则黑球数减1
    if y1[k]==1:
        s=n2-1
    else:
        s=n2   
    return s         
number1=0
#把刚才的程序重复N遍，计算频率
for i in range(N+1): 
    z=qiu()
    number1+=z
#第二个人取得黑球的概率
f1=number1/(N*(n-1)) 
print('模拟概率值为',f1,'理论概率值为',4/12)


