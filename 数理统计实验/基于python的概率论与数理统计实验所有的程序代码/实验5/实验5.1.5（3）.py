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
#计算组合数，定义组合函数为combinateC(n,m)
def combinateC(n,m):
    c=factorial(n)/(factorial(m)*factorial(n-m))
    return c
N=100
n=20
M=25
s=0
#计算超几何分布的分布律
for k in range(0,n):
    #超几何分布的分布律
    p=combinateC(M,k)*combinateC(N-M,n-k)/combinateC(N,n) 
    #画分布律图像
    plt.plot(k, p,linestyle='', marker='.')  
    plt.xlabel("k值")
    plt.ylabel("概率")
    plt.title("超几何分布的分布律,N=%d,M=%d,n=%d" % (N, M, n))
plt.show()

