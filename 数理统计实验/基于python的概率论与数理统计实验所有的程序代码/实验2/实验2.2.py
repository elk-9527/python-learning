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
#计算 
m=7
n=31
c=combinateC(n,m)
#计算中奖的概率
p1=1/c
p2=7/c
p3=combinateC(7,6)*combinateC(23,1)/c
p4=combinateC(7,5)*combinateC(23,1)/c
p5=(combinateC(7,5)*combinateC(23,2)+combinateC(7,4)*combinateC(23,2))/c
p6=(combinateC(7,4)*combinateC(23,3)+combinateC(7,3)*combinateC(23,3))/c
print(p1,p2,p3,p4,p5,p6)

