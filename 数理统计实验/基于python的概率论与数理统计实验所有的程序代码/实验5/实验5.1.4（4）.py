from matplotlib import pyplot as plt
#用来正常显示中文标签
plt.rcParams['font.sans-serif'] = [u'SimHei'] 
#用来正常显示正负号
plt.rcParams['axes.unicode_minus'] = False 
p=0.5
s=0
n=20
for k in range(1,n+1):
    #计算几何分布的分布律
    p1=((1-p)**(k-1))*p 
    #计算几何分布的分布函数
    s+=p1 
    #画分布函数图
    plt.plot(k, s,linestyle='', marker='.') 
    plt.xlabel("k值")
    plt.ylabel("概率")
    plt.title("几何分布的分布函数，参数p=%.2f" % p)
plt.show()
