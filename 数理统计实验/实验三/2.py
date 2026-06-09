import numpy as np
from scipy import stats

# 已知条件
mu0 = 0.5     # 原假设中的总体均值
x_bar = 0.452 # 样本均值
s = 0.035     # 样本标准差
n = 10        # 样本量
alpha = 0.05  # 显著性水平

# 计算检验统计量 t（总体标准差未知，用样本标准差）
t = (x_bar - mu0) / (s / np.sqrt(n))
print("检验统计量 t =", round(t, 4))

# 计算临界值（左侧单侧检验，自由度 df = n - 1）
df = n - 1
t_critical = stats.t.ppf(alpha, df)
print("临界值 t_alpha =", round(t_critical, 4))

# 计算 p 值（左侧单侧检验）
p_value = stats.t.cdf(t, df)
print("p 值 =", round(p_value, 6))

# 做出决策
print("\n=== 检验结果 ===")
if t < t_critical:
    print("拒绝原假设 H0（t =", round(t, 4), "< t临界值 =", round(t_critical, 4), ")")
    print("结论：在 alpha = 0.05 的显著性水平下，认为溶液中的水分含量低于0.5%。")
else:
    print("不拒绝原假设 H0（t =", round(t, 4), ">= t临界值 =", round(t_critical, 4), ")")
    print("结论：在 alpha = 0.05 的显著性水平下，没有足够证据表明溶液中的水分含量低于0.5%。")

if p_value < alpha:
    print("\np 值判断：拒绝原假设（p =", round(p_value, 6), "< alpha =", alpha, ")")
else:
    print("\np 值判断：不拒绝原假设（p =", round(p_value, 6), ">= alpha =", alpha, ")")