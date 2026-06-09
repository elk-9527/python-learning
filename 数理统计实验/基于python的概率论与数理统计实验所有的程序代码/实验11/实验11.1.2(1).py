import pandas as pd
import numpy as np
from scipy import stats
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm
# 所有的观测值
data=([[73,89,82,43,80,73,65,62,47,95,60,77]	,[88,78,48,91,54,	85,	74,	77,
50,78,65,76,	96,	80],[68,80,55,93,	72,	71,	87,	42,	61,	68,	53,	79,	15]])
# 方差的齐性检验
w, p = stats.levene(*data)
if p < 0.05:
    print('方差齐性假设不成立')
#把所有的样本观测值都写出来，形成列表
value = data[0].copy()
group= []
s=len(data)
for i in range(1,s):
    #extend() 函数用于在列表末尾一次性追加另一个序列中的多个值
    value.extend(data[i])  
print(value)
#为数据贴上标签，属于哪一组
for i, j in zip(range(3), data):
    group.extend(np.repeat('A'+str(i+1), len(j)).tolist())
print(group)
#把值和标签写成字典
dc = pd.DataFrame({'value': value, 'group': group}) 
a= anova_lm(ols('value~C(group)', dc).fit())
a.columns = ['自由度', '平方和', '均方', 'F值', 'P值']
a.index = ['因素A', '误差']
print(a)   


