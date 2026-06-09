import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams

rcParams['font.sans-serif'] = ['SimHei']
rcParams['axes.unicode_minus'] = False

def f(t):
    return 4 / (1 + t**2)

exact_value = np.pi


def trapezoidal(a, b):
    return (b - a) / 2 * (f(a) + f(b))


def simpson(a, b):
    c = (a + b) / 2
    return (b - a) / 6 * (f(a) + 4 * f(c) + f(b))


def composite_trapezoidal(a, b, n):
    h = (b - a) / n
    x = np.linspace(a, b, n + 1)
    y = f(x)
    return h / 2 * (y[0] + 2 * np.sum(y[1:-1]) + y[-1])


def composite_simpson(a, b, n):
    if n % 2 != 0:
        n += 1
    h = (b - a) / n
    x = np.linspace(a, b, n + 1)
    y = f(x)
    s_odd = np.sum(y[1:n:2])
    s_even = np.sum(y[2:n:2])
    return h / 3 * (y[0] + 4 * s_odd + 2 * s_even + y[-1])


def ml_poly_integral(a, b, degree=5, num_samples=100):
    t_samples = np.linspace(a, b, num_samples)
    v_samples = f(t_samples)
    coeffs = np.polyfit(t_samples, v_samples, degree)
    p = np.poly1d(coeffs)
    P = p.integ()
    return P(b) - P(a)


print("=" * 70)
print("数值积分实验：v(t) = 4/(1+t^2), 积分区间 [0,1], 精确值 = pi")
print("=" * 70)

T1 = trapezoidal(0, 1)
S1 = simpson(0, 1)
print(f"\n【基本求积公式】")
print(f"  梯形公式:     T = {T1:.10f}, 绝对误差 = {abs(T1 - exact_value):.6e}")
print(f"  辛普森公式:   S = {S1:.10f}, 绝对误差 = {abs(S1 - exact_value):.6e}")


ns = [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]
print(f"\n{'n':>6} | {'复化梯形':>14} | {'梯形误差':>14} | {'复化辛普森':>14} | {'辛普森误差':>14}")
print("-" * 76)

trap_errors = []
simp_errors = []

for n in ns:
    Tn = composite_trapezoidal(0, 1, n)
    Sn = composite_simpson(0, 1, n)
    err_T = abs(Tn - exact_value)
    err_S = abs(Sn - exact_value)
    trap_errors.append(err_T)
    simp_errors.append(err_S)
    print(f"{n:>6} | {Tn:>14.10f} | {err_T:>14.6e} | {Sn:>14.10f} | {err_S:>14.6e}")


print(f"\n【误差阶验证】")
for i in range(1, len(ns)):
    ratio_T = trap_errors[i-1] / trap_errors[i]
    ratio_S = simp_errors[i-1] / simp_errors[i]
    order_T = np.log2(ratio_T) if ratio_T > 0 else float('inf')
    order_S = np.log2(ratio_S) if ratio_S > 0 else float('inf')
    print(f"  n={ns[i]:>4}: 梯形误差比={ratio_T:.4f} (阶≈{order_T:.2f}), "
          f"辛普森误差比={ratio_S:.4f} (阶≈{order_S:.2f})")


print(f"\n【机器学习多项式拟合积分（选做）】")
for deg in [3, 5, 7, 9, 11]:
    for num in [20, 50, 100]:
        ml_val = ml_poly_integral(0, 1, degree=deg, num_samples=num)
        ml_err = abs(ml_val - exact_value)
        print(f"  阶数={deg:>2}, 采样点={num:>3}: 积分值={ml_val:.10f}, 误差={ml_err:.6e}")


fig, axes = plt.subplots(2, 2, figsize=(14, 10))

ax1 = axes[0, 0]
t = np.linspace(0, 1, 200)
ax1.plot(t, f(t), 'b-', linewidth=2, label='v(t)=4/(1+t²)')
ax1.fill_between(t, f(t), alpha=0.3, color='skyblue')
ax1.set_title('被积函数与积分区域', fontsize=13)
ax1.set_xlabel('t')
ax1.set_ylabel('v(t)')
ax1.legend()
ax1.grid(True, alpha=0.3)

ax2 = axes[0, 1]
n_demo = 4
h_demo = 1.0 / n_demo
x_demo = np.linspace(0, 1, n_demo + 1)
for i in range(n_demo):
    xi = np.linspace(x_demo[i], x_demo[i+1], 50)
    yi = f(x_demo[i]) + (f(x_demo[i+1]) - f(x_demo[i])) * (xi - x_demo[i]) / h_demo
    ax2.fill_between(xi, yi, alpha=0.3)
    ax2.plot(xi, yi, 'r-', linewidth=1.5)
ax2.plot(t, f(t), 'b-', linewidth=2, label='v(t)')
ax2.plot(x_demo, f(x_demo), 'ro', markersize=6)
ax2.set_title(f'复化梯形公式 (n={n_demo})', fontsize=13)
ax2.set_xlabel('t')
ax2.legend()
ax2.grid(True, alpha=0.3)

ax3 = axes[1, 0]
n_demo_s = 4
h_demo_s = 1.0 / n_demo_s
x_demo_s = np.linspace(0, 1, n_demo_s + 1)
for i in range(0, n_demo_s, 2):
    xi = np.linspace(x_demo_s[i], x_demo_s[i+2], 50)
    a_i, b_i, c_i = x_demo_s[i], x_demo_s[i+2], x_demo_s[i+1]
    L2 = (f(a_i) * (xi - c_i) * (xi - b_i) / ((a_i - c_i) * (a_i - b_i))
          + f(c_i) * (xi - a_i) * (xi - b_i) / ((c_i - a_i) * (c_i - b_i))
          + f(b_i) * (xi - a_i) * (xi - c_i) / ((b_i - a_i) * (b_i - c_i)))
    ax3.fill_between(xi, L2, alpha=0.3)
    ax3.plot(xi, L2, 'g-', linewidth=1.5)
ax3.plot(t, f(t), 'b-', linewidth=2, label='v(t)')
ax3.plot(x_demo_s, f(x_demo_s), 'go', markersize=6)
ax3.set_title(f'复化辛普森公式 (n={n_demo_s})', fontsize=13)
ax3.set_xlabel('t')
ax3.legend()
ax3.grid(True, alpha=0.3)

ax4 = axes[1, 1]
ax4.loglog(ns, trap_errors, 'ro-', linewidth=2, markersize=6, label='复化梯形误差')
ax4.loglog(ns, simp_errors, 'bs-', linewidth=2, markersize=6, label='复化辛普森误差')
h_vals = np.array([1.0/n for n in ns])
ax4.loglog(ns, h_vals**2 * trap_errors[0] / (1.0/ns[0])**2, 'r--', alpha=0.5, label='O(h²)参考线')
ax4.loglog(ns, h_vals**4 * simp_errors[0] / (1.0/ns[0])**4, 'b--', alpha=0.5, label='O(h⁴)参考线')
ax4.set_title('误差收敛速度对比', fontsize=13)
ax4.set_xlabel('n (等分数)')
ax4.set_ylabel('绝对误差')
ax4.legend()
ax4.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('数值积分实验结果.png', dpi=150, bbox_inches='tight')
plt.show()


fig2, ax = plt.subplots(1, 1, figsize=(10, 6))
methods = ['梯形公式', '辛普森公式', '复化梯形\n(n=1024)', '复化辛普森\n(n=1024)', 'ML拟合\n(deg=11)']
values = [
    trapezoidal(0, 1),
    simpson(0, 1),
    composite_trapezoidal(0, 1, 1024),
    composite_simpson(0, 1, 1024),
    ml_poly_integral(0, 1, degree=11, num_samples=100)
]
errors = [abs(v - exact_value) for v in values]
colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
bars = ax.bar(methods, errors, color=colors, edgecolor='black', linewidth=0.8)
ax.set_ylabel('绝对误差', fontsize=12)
ax.set_title('五种数值积分方法误差对比', fontsize=14)
ax.set_yscale('log')
for bar, err in zip(bars, errors):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() * 1.3,
            f'{err:.2e}', ha='center', va='bottom', fontsize=9)
ax.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.savefig('误差对比柱状图.png', dpi=150, bbox_inches='tight')
plt.show()
