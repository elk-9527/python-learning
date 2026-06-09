import numpy as np
from scipy import stats

# 样本数据（电池寿命）
data = np.array([73.2, 78.6, 75.4, 75.7, 74.1, 76.3, 72.8, 74.5, 76.6])

# 已知条件
sigma0 = 5      # 原假设中的标准差
n = len(data)   # 样本量
alpha = 0.01    # 显著性水平

# 计算样本统计量
x_bar = np.mean(data)
s = np.std(data, ddof=1)  # 样本标准差（使用ddof=1）
s_squared = s ** 2        # 样本方差
sigma0_squared = sigma0 ** 2  # 原假设中的方差

print("样本均值 =", round(x_bar, 4))
print("样本标准差 s =", round(s, 4))
print("样本方差 s^2 =", round(s_squared, 4))

# 计算卡方检验统计量
chi_squared = (n - 1) * s_squared / sigma0_squared
print("\n检验统计量 chi^2 =", round(chi_squared, 4))

# 计算临界值（左侧单侧检验，自由度 df = n - 1）
df = n - 1
chi_critical = stats.chi2.ppf(alpha, df)
print("临界值 chi^2_alpha =", round(chi_critical, 4))

# 计算 p 值（左侧单侧检验）
p_value = stats.chi2.cdf(chi_squared, df)
print("p 值 =", round(p_value, 6))

# 做出决策
print("\n=== 检验结果 ===")
if chi_squared < chi_critical:
    print("拒绝原假设 H0（chi^2 =", round(chi_squared, 4), "< chi^2临界值 =", round(chi_critical, 4), ")")
    print("结论：在 alpha = 0.01 的显著性水平下，认为这批电池的寿命标准差小于5，电池合格。")
else:
    print("不拒绝原假设 H0（chi^2 =", round(chi_squared, 4), ">= chi^2临界值 =", round(chi_critical, 4), ")")
    print("结论：在 alpha = 0.01 的显著性水平下，没有足够证据表明这批电池的寿命标准差小于5，电池不合格。")

if p_value < alpha:
    print("\np 值判断：拒绝原假设（p =", round(p_value, 6), "< alpha =", alpha, ")")
else:
    print("\np 值判断：不拒绝原假设（p =", round(p_value, 6), ">= alpha =", alpha, ")")