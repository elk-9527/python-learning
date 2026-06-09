import numpy as np
from scipy import stats

# 样本数据
old_method = np.array([75.5, 77.3, 76.2, 78.1, 74.3, 72.4, 77.4, 78.4, 76.7, 76.0])
new_method = np.array([77.3, 79.1, 79.1, 81.0, 80.2, 79.1, 82.1, 80.0, 77.3, 79.1])

# 已知条件
n1 = len(old_method)  # 旧法样本量
n2 = len(new_method)  # 新法样本量
alpha = 0.05          # 显著性水平

# 计算样本统计量
x_bar1 = np.mean(old_method)
x_bar2 = np.mean(new_method)
s1_squared = np.var(old_method, ddof=1)  # 样本方差（无偏估计）
s2_squared = np.var(new_method, ddof=1)

print("旧法样本均值 x̄₁ =", round(x_bar1, 4))
print("新法样本均值 x̄₂ =", round(x_bar2, 4))
print("旧法样本方差 s₁² =", round(s1_squared, 4))
print("新法样本方差 s₂² =", round(s2_squared, 4))

# 计算合并方差（方差相等时使用）
sp_squared = ((n1 - 1) * s1_squared + (n2 - 1) * s2_squared) / (n1 + n2 - 2)
print("\n合并方差 s_p² =", round(sp_squared, 4))

# 计算检验统计量 t（两总体方差未知但相等，双侧检验）
t = (x_bar1 - x_bar2) / np.sqrt(sp_squared * (1/n1 + 1/n2))
print("检验统计量 t =", round(t, 4))

# 计算自由度
df = n1 + n2 - 2
print("自由度 df =", df)

# 计算临界值（双侧检验）
t_critical = stats.t.ppf(1 - alpha/2, df)
print("临界值 t_alpha/2 = ±", round(t_critical, 4))

# 计算 p 值（双侧检验）
p_value = 2 * (1 - stats.t.cdf(np.abs(t), df))
print("p 值 =", round(p_value, 6))

# 做出决策
print("\n=== 检验结果 ===")
if np.abs(t) > t_critical:
    print("拒绝原假设 H0（|t| =", round(np.abs(t), 4), "> t临界值 =", round(t_critical, 4), ")")
    if t < 0:
        print("结论：在 alpha = 0.05 的显著性水平下，新法得率显著高于旧法。")
    else:
        print("结论：在 alpha = 0.05 的显著性水平下，新法得率显著低于旧法。")
else:
    print("不拒绝原假设 H0（|t| =", round(np.abs(t), 4), "<= t临界值 =", round(t_critical, 4), ")")
    print("结论：在 alpha = 0.05 的显著性水平下，没有足够证据表明新法与旧法得率有差异。")

if p_value < alpha:
    print("\np 值判断：拒绝原假设（p =", round(p_value, 6), "< alpha =", alpha, ")")
else:
    print("\np 值判断：不拒绝原假设（p =", round(p_value, 6), ">= alpha =", alpha, ")")
