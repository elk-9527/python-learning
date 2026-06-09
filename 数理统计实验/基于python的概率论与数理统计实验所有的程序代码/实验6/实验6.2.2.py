from scipy.stats import norm
mu1=3
sigma1=2
#计算第一问
p=norm.cdf(5,mu1,sigma1)-norm.cdf(2,mu1,sigma1) 
y=norm.ppf(0.5) 
#计算第二问
C=y*sigma1+mu1 
#计算第三问
z=norm.ppf(0.1,mu1,sigma1) 
print(p,C,z)


