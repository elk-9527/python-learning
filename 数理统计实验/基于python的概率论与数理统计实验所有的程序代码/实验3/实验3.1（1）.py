import math
from scipy import stats
# 两平行线间的距离
d = 1
# 针长
l = 0.83           
# 计数器用来统计针与线相交的次数               
counter = 0  
# 投针次数                         
N = 100000                          
# 针的中点到平行线的距离，在此设其服从区间[0,d/2]上的均匀分布
x = stats.uniform.rvs(0, d/2, size=N)       
# 针与平行线的夹角，在此设其服从区间[0, pi/2]上的均匀分布
phi = stats.uniform.rvs(0, math.pi/2, size=N) 
for i in range(1, N):
    # 满足此条件表示投出的针与平行线相交
    if x[i-1] < l * math.sin(phi[i-1]) / 2:  
        counter = counter+1
# 计算针与平行线相交的频率
fren = counter/N   
# 计算π的近似值                     
pi_hat = 2*l/(d*fren)                   
print(pi_hat)


