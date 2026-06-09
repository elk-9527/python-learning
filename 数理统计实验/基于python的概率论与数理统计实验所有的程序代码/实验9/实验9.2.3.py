# 导入scipy.stats库，用于统计计算
import scipy.stats as st

# 样本数据：6个观测值
data=[6.683,6.681,6.676,6.678,6.679,6.672]

def onekafanginterval(mu,confidence):
    """
    计算正态总体方差的置信区间
    
    参数说明：
    mu: 总体期望，如果为None表示期望未知
    confidence: 置信水平（如0.9表示90%置信度）
    
    返回值：
    (lower, upper): 方差的置信区间下限和上限
    """
    
    # 计算显著性水平α（alpha）
    alpha=1-confidence
    
    # 获取样本容量
    n=len(data)
    
    # 计算卡方分布的分位数（期望未知的情况，自由度为n-1）
    # χ²_{1-α/2}(n-1)：上α/2分位数
    kf_percentile1=st.chi2.ppf(1-alpha/2,n-1)
    # χ²_{α/2}(n-1)：下α/2分位数
    kf_percentile2=st.chi2.ppf(alpha/2,n-1)
    
    # 计算卡方分布的分位数（期望已知的情况，自由度为n）
    # χ²_{1-α/2}(n)：上α/2分位数
    kf_percentile3=st.chi2.ppf(1-alpha/2,n)
    # χ²_{α/2}(n)：下α/2分位数
    kf_percentile4=st.chi2.ppf(alpha/2,n)
    
    # 初始化累加变量
    s1=0  # 用于计算样本均值
    s2=0  # 用于计算样本方差（期望未知时）
    s3=0  # 用于计算平方和（期望已知时）
    
    # 情况1：期望未知，求方差的置信区间（小样本 n<30）
    # 统计学原理：(n-1)S²/σ² ~ χ²(n-1)
    if n<30 and mu==None:
        # 计算样本均值
        for i in range(0,n):
            k=data[i]
            s1=s1+k 
        mean=s1/n    
        
        # 计算样本方差（实际上是平方和 Σ(xᵢ - x̄)²）
        for i in range(0,n):
           k=data[i]
           s2=s2+(k-mean)**2   
        
        # 计算置信区间
        # 下限：Σ(xᵢ - x̄)² / χ²_{1-α/2}(n-1)
        lower=s2/kf_percentile1
        # 上限：Σ(xᵢ - x̄)² / χ²_{α/2}(n-1)
        upper=s2/kf_percentile2
    
    # 情况2：期望已知，求方差的置信区间（小样本 n<30）
    # 统计学原理：Σ(xᵢ - μ)²/σ² ~ χ²(n)
    if n<30 and mu!=None:
        # 计算平方和 Σ(xᵢ - μ)²
         for i in range(0,n):
            k=data[i]
            s3=s3+(k-mu)**2  
         
         # 计算置信区间
         # 下限：Σ(xᵢ - μ)² / χ²_{1-α/2}(n)
         lower=s3/kf_percentile3
         # 上限：Σ(xᵢ - μ)² / χ²_{α/2}(n)
         upper=s3/kf_percentile4
    
    # 返回置信区间（下限，上限）
    return(lower,upper)

# 调用函数：期望未知（mu=None），置信水平为90%
b=onekafanginterval(None,0.9)

# 输出结果
print('置信区间为',b)