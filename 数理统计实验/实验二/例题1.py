import numpy as np
import scipy.stats as st

data = [14.6, 15.1, 14.9, 14.8, 15.2, 15.1, 14.8, 15.0, 14.7]
def norm_mean_interval(sigma, confidence_level):
    alpha = 1 - confidence_level
    n = len(data)
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

a = norm_mean_interval(sigma = 1, confidence_level = 0.95)
print('置信区间',a)