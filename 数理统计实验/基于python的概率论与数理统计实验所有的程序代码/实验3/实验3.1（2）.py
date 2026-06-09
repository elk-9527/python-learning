import math
import random
pai=3.1415926535
# 两平行线间的距离
d = 1 
# 针长                       
l = 0.83
 # 投针次数                          
N = 500000  
# 计数器用来统计平行线线相交的针的个数                    
number=0                      
#cx表示针的中点的横坐标，cy表示针的中点的纵坐标。
for i in range(1, N+1):
    #针的中点的横坐标范围为[0，d/2)
    cx=0.5*d*random.random()
    #针的中点的纵坐标范围为[0，d/2)
    cy=0.5*d*random.random()
    #针与平行线的夹角为[0, π)
    phi=pai*random.random()
    #针的一端到最近的平行线的距离
    y1=cy+0.5*l*math.sin(phi) 
    #针的另一端到最近的平行线的距离
    y2=cy-0.5*l*math.sin(phi) 
    # 满足此条件表示投出的针与平行线相交
    if y1 >d or y2 < 0: 
       number+=1
#计算针与平行线相交的理论概率值
probility=2*l/(pai*d)  
# 计算投出的针与平行线相交的频率                  
frequency = number/N 
# 计算π的近似值                  
pai_hat = 2*l/(d*frequency)              
print(probility,frequency,pai_hat)


