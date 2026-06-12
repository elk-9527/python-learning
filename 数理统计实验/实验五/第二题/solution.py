import numpy as np
from scipy import stats

# 数据
x = np.array([0, 4, 10, 15, 21, 29, 36, 51, 68])
y = np.array([66.7, 71.0, 76.3, 80.6, 85.7, 92.9, 99.4, 113.6, 125.1])

n = len(x)

# 计算基本统计量
x_mean = np.mean(x)
y_mean = np.mean(y)

# 计算回归系数
SS_xx = np.sum((x - x_mean) ** 2)
SS_xy = np.sum((x - x_mean) * (y - y_mean))
SS_yy = np.sum((y - y_mean) ** 2)

beta_1 = SS_xy / SS_xx
beta_0 = y_mean - beta_1 * x_mean

print("=" * 60)
print("(1) 线性回归方程")
print("=" * 60)
print("回归系数 beta_1 =", round(beta_1, 4))
print("截距 beta_0 =", round(beta_0, 4))
print("线性回归方程: y =", round(beta_0, 4), "+", round(beta_1, 4), "x")
print()

# (2) F 检验
# 计算 SSR, SSE, SST
SSR = beta_1 * SS_xy
SSE = SS_yy - SSR
SST = SS_yy

# 自由度
df_R = 1
df_E = n - 2
df_T = n - 1

# 均方
MSR = SSR / df_R
MSE = SSE / df_E

# F 值
F = MSR / MSE

# 临界值
alpha = 0.05
F_critical = stats.f.ppf(1 - alpha, df_R, df_E)

print("=" * 60)
print("(2) F 检验法检验线性回归效果的显著性")
print("=" * 60)
print("SSR (回归平方和) =", round(SSR, 4))
print("SSE (残差平方和) =", round(SSE, 4))
print("SST (总平方和) =", round(SST, 4))
print("F 值 =", round(F, 4))
print("F 临界值 (alpha=0.05, df1=%d, df2=%d) =" % (df_R, df_E), round(F_critical, 4))
print("p 值 =", round(1 - stats.f.cdf(F, df_R, df_E), 6))
if F > F_critical:
    print("结论：拒绝原假设，线性回归效果显著")
else:
    print("结论：接受原假设，线性回归效果不显著")
print()

# (3) 预测区间
x0 = 70
y0_pred = beta_0 + beta_1 * x0

# 预测区间公式
t_critical = stats.t.ppf(1 - alpha/2, df_E)
s_e = np.sqrt(MSE)

prediction_interval = t_critical * s_e * np.sqrt(1 + 1/n + (x0 - x_mean)**2 / SS_xx)

print("=" * 60)
print("(3) x0 = 70 时，y0 的概率为 0.95 的预测区间")
print("=" * 60)
print("预测值 y_hat =", round(y0_pred, 4))
print("预测区间: (", round(y0_pred - prediction_interval, 4), ",", round(y0_pred + prediction_interval, 4), ")")
print()

# (4) 置信区间
confidence_interval = t_critical * s_e * np.sqrt(1/n + (x0 - x_mean)**2 / SS_xx)

print("=" * 60)
print("(4) E(y0) = beta_0 + beta_1*x0 的置信水平为 0.95 的置信区间")
print("=" * 60)
print("E(y0) 的估计值 =", round(y0_pred, 4))
print("置信区间: (", round(y0_pred - confidence_interval, 4), ",", round(y0_pred + confidence_interval, 4), ")")
print()

print("=" * 60)
print("总结")
print("=" * 60)
print("线性回归方程: y =", round(beta_0, 4), "+", round(beta_1, 4), "x")
print("F 检验结果: F =", round(F, 4), "> F_0.05(%d,%d) =" % (df_R, df_E), round(F_critical, 4), "，回归效果显著")
print("x0=70 时的预测区间: (", round(y0_pred - prediction_interval, 4), ",", round(y0_pred + prediction_interval, 4), ")")
print("E(y0) 的置信区间: (", round(y0_pred - confidence_interval, 4), ",", round(y0_pred + confidence_interval, 4), ")")