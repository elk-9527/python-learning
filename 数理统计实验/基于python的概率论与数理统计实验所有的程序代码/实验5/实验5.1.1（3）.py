from matplotlib import pyplot as plt
#用来正常显示中文标签
plt.rcParams['font.sans-serif'] = [u'SimHei'] 
#用来正常显示正负号
plt.rcParams['axes.unicode_minus'] = False 
#计算阶乘，定义阶乘函数为factorial
def factorial(n):
    s=1
    for i in range(1,n+1):
        s=s*i
    return s
#计算组合数
def combinateC(n,m):
    c=factorial(n)/(factorial(m)*factorial(n-m))
    return c
n=60
p=0.5
s=0
#计算二项分布的分布律
for k in range(0,n+1):
    c=combinateC(n,k)
    #计算二项分布的分布律
    p1=c*p**k*(1-p)**(n-k) 
    #画分布律图
    plt.plot(k, p1,linestyle='', marker='.')  
plt.title("二项分布的分布律，n=%d,p=%.2f" % (n,p))
plt.show()


