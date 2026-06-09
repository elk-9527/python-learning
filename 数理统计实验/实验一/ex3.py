import sympy as sp

# 定义符号变量
lambda_ = sp.Symbol('lambda', positive=True)
k = sp.Symbol('k', integer=True, nonnegative=True)

# 泊松分布的概率质量函数 P(X=k) = e^(-lambda) * lambda^k / k!
pmf = sp.exp(-lambda_) * (lambda_ ** k) / sp.factorial(k)
print(f"泊松分布的概率质量函数: P(X=k) = {pmf}")

# 样本观测值（题目中写容量为6，但给出了7个数据，这里按实际数据处理）
data = [1, 2, 2, 1, 1, 5, 1]
n = len(data)
print(f"样本观测值: {data}")
print(f"样本容量 n = {n}")

# 计算样本均值（泊松分布中lambda的极大似然估计就是样本均值）
sample_mean = sum(data) / n
print(f"样本均值 = {sample_mean}")
print(f"参数 lambda 的极大似然估计值 = {sample_mean}")

# 极大似然估计的推导过程
print("\n--- 极大似然估计推导过程 ---")
# 似然函数 L(lambda) = 乘积 P(X_i = x_i)
log_likelihood = sum([sp.log(pmf.subs(k, xi)) for xi in data])
print(f"对数似然函数: lnL(lambda) = {sp.simplify(log_likelihood)}")

# 对lambda求导并令导数为0
d_log_likelihood = sp.diff(log_likelihood, lambda_)
print(f"对数似然函数的导数: d(lnL)/d(lambda) = {sp.simplify(d_log_likelihood)}")

# 解方程求极大似然估计
equation = sp.Eq(d_log_likelihood, 0)
lambda_hat = sp.solve(equation, lambda_)[0]
print(f"解方程得 lambda 的极大似然估计值: lambda_hat = {lambda_hat}")
