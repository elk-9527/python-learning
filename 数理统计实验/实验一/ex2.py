import sympy as sp

# 定义符号 (theta > -1)
theta = sp.Symbol('theta')
x = sp.Symbol('x')

# 总体密度函数 f(x) = (theta+1)*x^theta, 0<x<1
# 计算总体期望 E(X) = ∫(0,1) x*(theta+1)*x^theta dx = (theta+1)/(theta+2)
EX = (theta + 1) / (theta + 2)
print(f"总体期望 E(X) = {EX}")

# 样本观测值
data = [0.1, 0.4, 0.5, 0.3, 0.2]
n = len(data)
sample_mean = sum(data) / n
print(f"样本均值 = {sample_mean}")

# 矩估计：令 E(X) = 样本均值，解出 theta
equation = sp.Eq(EX, sample_mean)
theta_hat = sp.solve(equation, theta)[0]
print(f"theta 的矩估计值 = {theta_hat}")
print(f"theta 的矩估计值 (小数) = {float(theta_hat)}")
