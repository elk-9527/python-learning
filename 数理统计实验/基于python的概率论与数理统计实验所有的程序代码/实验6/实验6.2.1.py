from scipy.stats import norm
mu=170
sigma=6
x=norm.ppf(0.95)
h=x*6+mu
print(h)

