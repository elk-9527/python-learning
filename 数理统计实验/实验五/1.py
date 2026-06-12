import numpy as np

# 实验数据
x = np.array([150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 250, 260])
y = np.array([56.9, 58.3, 61.6, 64.6, 68.1, 71.3, 74.1, 77.4, 80.2, 82.6, 86.4, 89.7])
n = len(x)

# 计算基础统计量
sum_x = np.sum(x)
sum_y = np.sum(y)
sum_xy = np.sum(x * y)
sum_x2 = np.sum(x ** 2)
sum_y2 = np.sum(y ** 2)

# 计算回归系数 b 和截距 a
b = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x ** 2)
a = (sum_y - b * sum_x) / n

print("=" * 50)
print("(1) 线性回归方程")
print("=" * 50)
print(f"线性回归方程：y = {a:.4f} + {b:.4f}x")

# F 检验
y_mean = np.mean(y)
y_hat = a + b * x

# 回归平方和
SSR = np.sum((y_hat - y_mean) ** 2)
# 残差平方和
SSE = np.sum((y - y_hat) ** 2)
# 总平方和
SST = np.sum((y - y_mean) ** 2)

# F 统计量
F = (SSR / 1) / (SSE / (n - 2))

# F临界值（查表得到，自由度 df1=1, df2=10, α=0.05）
F_critical = 4.96

print("\n" + "=" * 50)
print("(2) F 检验结果")
print("=" * 50)
print(f"SSR = {SSR:.4f}")
print(f"SSE = {SSE:.4f}")
print(f"SST = {SST:.4f}")
print(f"F = {F:.4f}")
print(f"F 临界值（α=0.05）= {F_critical:.4f}")
print(f"显著性检验：{'回归效果显著' if F > F_critical else '回归效果不显著'}")

# (3) 预测区间
x0 = 225
y_hat0 = a + b * x0

# 残差标准差
s_e = np.sqrt(SSE / (n - 2))

# S_xx
S_xx = sum_x2 - sum_x ** 2 / n

# t分布分位数（查表得到，自由度 n-2=10, α=0.05/2）
t_alpha2 = 2.228

# 预测区间半径
radius = t_alpha2 * s_e * np.sqrt(1 + 1/n + (x0 - sum_x/n)**2 / S_xx)

# 预测区间
lower = y_hat0 - radius
upper = y_hat0 + radius

print("\n" + "=" * 50)
print("(3) 预测区间")
print("=" * 50)
print(f"当 x0 = {x0} 时：")
print(f"点预测值 y_hat0 = {y_hat0:.4f}")
print(f"残差标准差 s_e = {s_e:.4f}")
print(f"预测区间半径 = {radius:.4f}")
print(f"95% 预测区间：[{lower:.4f}, {upper:.4f}]")
