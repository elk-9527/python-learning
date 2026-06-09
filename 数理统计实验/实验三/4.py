import numpy as np
from scipy import stats

# 样本数据
A = np.array([24, 27, 26, 21, 24])
B = np.array([27, 28, 23, 31, 26])

# 已知条件
var_A = 5     # A种烟草总体方差（已知）
var_B = 8     # B种烟草总体方差（已知）
n_A = len(A)  # 样本A的样本量
n_B = len(B)  # 样本B的样本量
alpha = 0.05  # 显著性水平

# 计算样本均值
x_bar_A = np.mean(A)
x_bar_B = np.mean(B)
# round 是四舍五入函数，保留两位小数
print("样本A均值 x̄_A =", round(x_bar_A, 2))
print("样本B均值 x̄_B =", round(x_bar_B, 2))

# 计算检验统计量 Z（两总体方差已知，双侧检验）
Z = (x_bar_A - x_bar_B) / np.sqrt(var_A/n_A + var_B/n_B)
print("检验统计量 Z =", round(Z, 4))

# 计算临界值（双侧检验）
z_critical = stats.norm.ppf(1 - alpha/2)
print("临界值 Z_alpha/2 = ±", round(z_critical, 4))

# 计算 p 值（双侧检验）
# .cdf 是累计分布函数，返回小于等于给定值的概率密度
# 1 - .cdf 是大于给定值的概率密度
p_value = 2 * (1 - stats.norm.cdf(np.abs(Z)))
print("p 值 =", round(p_value, 6))

# 做出决策
print("\n=== 检验结果 ===")
if np.abs(Z) > z_critical:
    print("拒绝原假设 H0（|Z| =", round(np.abs(Z), 4), "> Z临界值 =", round(z_critical, 4), ")")
    print("结论：在 alpha = 0.05 的显著性水平下，认为两种烟草的尼古丁含量有差异。")
else:
    print("不拒绝原假设 H0（|Z| =", round(np.abs(Z), 4), "<= Z临界值 =", round(z_critical, 4), ")")
    print("结论：在 alpha = 0.05 的显著性水平下，没有足够证据表明两种烟草的尼古丁含量有差异。")

if p_value < alpha:
    print("\np 值判断：拒绝原假设（p =", round(p_value, 6), "< alpha =", alpha, ")")
else:
    print("\np 值判断：不拒绝原假设（p =", round(p_value, 6), ">= alpha =", alpha, ")")
