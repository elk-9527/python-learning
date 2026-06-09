from scipy import stats
A1 = [73,89,82,43,80,73,65,62,47,95,60,77]
A2 = [88,78,48,91,54,	85,	74,	77,	50,78,65,	76,	96,	80]
A3 = [68,80,55,93,	72,	71,	87,	42,	61,	68,	53,	79,	15]
data = [A1, A2, A3]
#F方差齐性检验
w, p = stats.levene(*data)
if p < 0.05:
    print('方差齐性假设不成立')
# 方差齐性成立之后， 就可以进行单因素方差分析   
F, p = stats.f_oneway(A1, A2, A3)
#计算当alpha=0.05,自由度为（2，21）时F分位数的大小
F_percentile = stats.f.ppf((1-0.05), 2, 21) 
print('F值是%.2f，p值是%.9f' % (F,p))
print('F_ percentile的值是%.2f' % (F_percentile ))
#比较F值与分位数F_percentile的大小
if F>=F_percentile:
    print('拒绝原假设，有显著性差异')
else:
    print('接受原假设，无显著性差异')

