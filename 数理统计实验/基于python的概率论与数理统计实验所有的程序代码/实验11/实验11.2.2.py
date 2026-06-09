import statsmodels.api as sm
X=[100,110,120,130,140,150,160,170,180,190]
Y=[45,	51,	54,	61,	66,	70,	74,	78,	85,	89]
# 向 x1 左侧添加截距列 x0=[1,...1]
X1 = sm.add_constant(X) 
# 建立最小二乘模型（OLS）
model = sm.OLS(Y, X1) 
# 返回模型拟合结果
results = model.fit()
# 输出回归分析的摘要
print(results.summary())



