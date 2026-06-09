import numpy as np
import scipy.stats as st

data = [14.6, 15.1, 14.9, 14.8, 15.2, 15.1, 14.8, 15.0, 14.7]

def norm_mean_interval(sigma, confidence_level):
    alpha = 1 - confidence_level
    n = len(data)
    # .ppf() 的作用是： 根据给定的累积概率，找到对应的分位数值 。
    z_percentile = st.norm.ppf(1 - alpha / 2)
    # 计算均值
    s1 = 0
    for i in range(n):
        k = data[i]
        s1 = s1 + k
    mean = s1 / n
    # 方差已知，求mu的置信区间
    lower = mean - z_percentile * sigma / np.sqrt(n)
    upper = mean + z_percentile * sigma / np.sqrt(n)
    return lower, upper

# 题目中给出方差为0.05，所以标准差sigma = sqrt(0.05)
a = norm_mean_interval(sigma=np.sqrt(0.05), confidence_level=0.95)
print(f"平均长度μ的95%置信区间为：({a[0]:.4f}, {a[1]:.4f})")
