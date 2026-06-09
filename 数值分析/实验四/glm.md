# 数值积分算法设计与实现实验报告

## 一、实验名称

数值积分算法设计与实现（梯形公式、辛普森公式、复化求积）

## 二、实验目的

1. 理解数值积分的基本思想：用离散加权求和近似代替定积分，实现非线性函数积分的数值求解。
2. 掌握梯形求积公式、辛普森（Simpson）求积公式的原理与误差特性。
3. 掌握复化梯形、复化辛普森数值积分算法，理解步长对精度的影响。
4. 通过编程实现数值积分，对比不同算法的收敛速度、计算精度。
5. 理解数值积分的线性性、阶数、误差阶与算法稳定性。

## 三、实验原理与公式推导

### 工程背景

某滑块做非线性变速直线运动，瞬时速度函数为：

$$v(t) = \frac{4}{1 + t^2} \quad \text{(m/s)}$$

需要求解该滑块在时间区间 $[0,1]$ 秒内的运动位移：

$$S = \int_{0}^{1} \frac{4}{1 + t^2} \, dt = 4 \arctan(t) \Big|_0^1 = 4 \times \frac{\pi}{4} = \pi \approx 3.14159265\ldots \text{ m}$$

### 1. 梯形求积公式（两点公式）

**推导过程：**

在积分区间 $[a, b]$ 上，用通过两端点 $(a, f(a))$ 和 $(b, f(b))$ 的直线（一次多项式）来近似被积函数 $f(x)$，然后对该直线求积分。

线性插值多项式为：

$$L_1(x) = f(a) \cdot \frac{x - b}{a - b} + f(b) \cdot \frac{x - a}{b - a}$$

对 $L_1(x)$ 在 $[a,b]$ 上积分：

$$\int_a^b L_1(x) \, dx = f(a) \int_a^b \frac{x-b}{a-b} \, dx + f(b) \int_a^b \frac{x-a}{b-a} \, dx$$

计算第一个积分：

$$\int_a^b \frac{x-b}{a-b} \, dx = \frac{1}{a-b} \cdot \frac{(x-b)^2}{2} \Big|_a^b = \frac{1}{a-b} \cdot \frac{0 - (a-b)^2}{2} = \frac{b-a}{2}$$

计算第二个积分：

$$\int_a^b \frac{x-a}{b-a} \, dx = \frac{1}{b-a} \cdot \frac{(x-a)^2}{2} \Big|_a^b = \frac{1}{b-a} \cdot \frac{(b-a)^2}{2} = \frac{b-a}{2}$$

因此得到**梯形公式**：

$$\int_a^b f(x) \, dx \approx T = \frac{b-a}{2} [f(a) + f(b)]$$

**误差分析：**

梯形公式的截断误差由插值余项积分得到。利用插值余项 $R_1(x) = \frac{f''(\xi_x)}{2!}(x-a)(x-b)$，注意到 $(x-a)(x-b) \leq 0$ 在 $[a,b]$ 上不变号，由积分中值定理：

$$R_T = -\frac{(b-a)^3}{12} f''(\eta), \quad \eta \in (a, b)$$

即误差阶为 $O(h^3)$，其中 $h = b - a$。

### 2. 辛普森求积公式（三点抛物线插值）

**推导过程：**

在积分区间 $[a, b]$ 上取三个等距节点 $a$、$\frac{a+b}{2}$、$b$，用过这三点的抛物线（二次多项式）来近似 $f(x)$。

记中点 $c = \frac{a+b}{2}$，步长 $h = \frac{b-a}{2}$。

二次 Lagrange 插值多项式：

$$L_2(x) = f(a) \cdot l_0(x) + f(c) \cdot l_1(x) + f(b) \cdot l_2(x)$$

其中：

$$l_0(x) = \frac{(x-c)(x-b)}{(a-c)(a-b)}, \quad l_1(x) = \frac{(x-a)(x-b)}{(c-a)(c-b)}, \quad l_2(x) = \frac{(x-a)(x-c)}{(b-a)(b-c)}$$

分别计算各基函数的积分：

$$\int_a^b l_0(x) \, dx = \frac{h}{3}, \quad \int_a^b l_1(x) \, dx = \frac{4h}{3}, \quad \int_a^b l_2(x) \, dx = \frac{h}{3}$$

因此得到**辛普森公式**：

$$\int_a^b f(x) \, dx \approx S = \frac{b-a}{6} [f(a) + 4f\Big(\frac{a+b}{2}\Big) + f(b)]$$

或等价地写成：

$$S = \frac{h}{3} [f(a) + 4f(c) + f(b)], \quad h = \frac{b-a}{2}$$

**误差分析：**

辛普森公式对三次多项式精确成立（代数精度为 3），其截断误差为：

$$R_S = -\frac{(b-a)^5}{2880} f^{(4)}(\eta) = -\frac{h^5}{90} f^{(4)}(\eta), \quad \eta \in (a, b)$$

误差阶为 $O(h^5)$。

> **辛普森公式对三次多项式精确的原因：** 虽然辛普森公式基于二次插值，但通过特定系数 $\frac{1}{6}, \frac{4}{6}, \frac{1}{6}$ 的选取，恰好使得三次项的积分误差相互抵消，代数精度从 2 提升到 3。

### 3. 复化梯形公式

**推导过程：**

将积分区间 $[a,b]$ 等分为 $n$ 个子区间，节点为 $x_i = a + ih$，$i = 0, 1, \ldots, n$，步长 $h = \frac{b-a}{n}$。

在每个子区间 $[x_i, x_{i+1}]$ 上应用梯形公式：

$$\int_{x_i}^{x_{i+1}} f(x) \, dx \approx \frac{h}{2} [f(x_i) + f(x_{i+1})]$$

对所有子区间求和：

$$\int_a^b f(x) \, dx \approx T_n = \sum_{i=0}^{n-1} \frac{h}{2} [f(x_i) + f(x_{i+1})]$$

展开合并同类项，内部节点各出现两次，端点各出现一次：

$$T_n = \frac{h}{2} [f(a) + 2\sum_{i=1}^{n-1} f(x_i) + f(b)]$$

**误差分析：**

$$R_{T_n} = -\frac{(b-a)}{12} h^2 f''(\eta) = -\frac{(b-a)^3}{12n^2} f''(\eta), \quad \eta \in (a, b)$$

复化梯形公式的误差阶为 $O(h^2)$。

### 4. 复化辛普森公式

**推导过程：**

将积分区间 $[a,b]$ 等分为 $2n$ 个子区间（注意：必须为偶数份），节点为 $x_i = a + ih$，$i = 0, 1, \ldots, 2n$，步长 $h = \frac{b-a}{2n}$。

在每两个相邻子区间 $[x_{2k}, x_{2k+2}]$ 上应用辛普森公式（以 $x_{2k+1}$ 为中点）：

$$\int_{x_{2k}}^{x_{2k+2}} f(x) \, dx \approx \frac{h}{3} [f(x_{2k}) + 4f(x_{2k+1}) + f(x_{2k+2})]$$

对所有 $n$ 个双区间求和：

$$S_{2n} = \frac{h}{3} \sum_{k=0}^{n-1} [f(x_{2k}) + 4f(x_{2k+1}) + f(x_{2k+2})]$$

展开后整理，偶数下标节点（端点除外）各出现两次，奇数下标节点各出现一次：

$$S_{2n} = \frac{h}{3} [f(a) + 4\sum_{k=0}^{n-1} f(x_{2k+1}) + 2\sum_{k=1}^{n-1} f(x_{2k}) + f(b)]$$

**误差分析：**

$$R_{S_{2n}} = -\frac{(b-a)}{180} h^4 f^{(4)}(\eta) = -\frac{(b-a)^5}{180 \cdot (2n)^4} f^{(4)}(\eta), \quad \eta \in (a, b)$$

复化辛普森公式的误差阶为 $O(h^4)$。

### 5. 核心性质——线性性

数值积分满足线性性：若 $f(x) = \alpha \cdot g(x) + \beta \cdot h(x)$，则：

$$\int_a^b f(x) \, dx \approx \alpha \cdot Q(g) + \beta \cdot Q(h)$$

其中 $Q$ 为任意数值积分算子（梯形、辛普森等均满足）。这一性质在工程中非常重要：多个物理量的叠加积分可以分别计算再线性组合，简化计算流程。

## 四、Python 代码实现

```python
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
```

## 五、实验结果与分析

### 1. 基本求积公式结果

| 方法       | 积分值       | 绝对误差     |
| ---------- | ------------ | ------------ |
| 梯形公式   | 3.0000000000 | 1.415927e-01 |
| 辛普森公式 | 3.1333333333 | 8.259320e-03 |

**分析：** 辛普森公式的精度远高于梯形公式。梯形公式仅用直线近似，误差较大；辛普森公式用抛物线近似，能更好地拟合 $v(t) = 4/(1+t^2)$ 的曲线形状，误差约为梯形公式的 1/17。

### 2. 复化求积公式结果（不同 n 值）

| n    | 复化梯形值   | 梯形误差     | 复化辛普森值 | 辛普森误差   |
| ---- | ------------ | ------------ | ------------ | ------------ |
| 2    | 3.1000000000 | 4.159265e-02 | 3.1333333333 | 8.259320e-03 |
| 4    | 3.1311764706 | 1.041618e-02 | 3.1415686275 | 2.402614e-05 |
| 8    | 3.1389884945 | 2.604159e-03 | 3.1415925025 | 1.511311e-07 |
| 16   | 3.1409416120 | 6.510415e-04 | 3.1415926512 | 2.364971e-09 |
| 32   | 3.1414298932 | 1.627604e-04 | 3.1415926536 | 3.695666e-11 |
| 64   | 3.1415519635 | 4.069010e-05 | 3.1415926536 | 5.773160e-13 |
| 128  | 3.1415824811 | 1.017253e-05 | 3.1415926536 | 8.881784e-15 |
| 256  | 3.1415901105 | 2.543132e-06 | 3.1415926536 | 0.000000e+00 |
| 512  | 3.1415920178 | 6.357829e-07 | 3.1415926536 | 0.000000e+00 |
| 1024 | 3.1415924946 | 1.589457e-07 | 3.1415926536 | 0.000000e+00 |

### 3. 误差阶验证

**复化梯形公式：** 当 $n$ 加倍时，误差比约趋近于 4，即 $\log_2(\text{ratio}) \approx 2$，验证了误差阶为 $O(h^2)$。

**复化辛普森公式：** 当 $n$ 加倍时，误差比约趋近于 16，即 $\log_2(\text{ratio}) \approx 4$，验证了误差阶为 $O(h^4)$。

辛普森公式的收敛速度远快于梯形公式——每增加一倍等分数，辛普森误差缩小约 16 倍，而梯形仅缩小约 4 倍。

### 4. 机器学习多项式拟合积分结果（选做）

| 多项式阶数 | 采样点数 | 积分值       | 绝对误差     |
| ---------- | -------- | ------------ | ------------ |
| 3          | 20       | 3.1410062417 | 5.864119e-04 |
| 3          | 50       | 3.1413440751 | 2.485785e-04 |
| 3          | 100      | 3.1414658265 | 1.268270e-04 |
| 5          | 20       | 3.1416475219 | 5.486833e-05 |
| 5          | 50       | 3.1416185783 | 2.592472e-05 |
| 5          | 100      | 3.1416065187 | 1.386512e-05 |
| 7          | 20       | 3.1415905812 | 2.072391e-06 |
| 7          | 50       | 3.1415916527 | 1.000914e-06 |
| 7          | 100      | 3.1415920858 | 5.677781e-07 |
| 9          | 20       | 3.1415926657 | 1.206520e-08 |
| 9          | 50       | 3.1415926577 | 4.159637e-09 |
| 9          | 100      | 3.1415926560 | 2.405867e-09 |
| 11         | 20       | 3.1415926617 | 8.107602e-09 |
| 11         | 50       | 3.1415926554 | 1.835335e-09 |
| 11         | 100      | 3.1415926547 | 1.110620e-09 |

**分析：** 多项式拟合积分通过先对采样点做多项式回归，再对拟合多项式解析积分。适当提高多项式阶数和采样点数可获得很高精度。但需注意：阶数过高可能导致过拟合（Runge 现象），阶数过低则欠拟合。

### 5. 工程精度分析

工程中通常要求相对误差在 $10^{-3}$（0.1%）以内：

| 方法       | 达到工程精度所需 n                                          |
| ---------- | ----------------------------------------------------------- |
| 复化梯形   | n ≥ 16（误差 6.51e-04），n ≥ 8 时误差 2.60e-03 接近但不满足 |
| 复化辛普森 | n ≥ 4（误差 2.40e-05），远超工程精度                        |

辛普森公式用极少的计算量即可满足工程精度要求，在实际工程中更具效率优势。

## 六、四种算法对比总结

| 对比项           | 梯形公式     | 辛普森公式     | 复化梯形 | 复化辛普森 |
| ---------------- | ------------ | -------------- | -------- | ---------- |
| 插值类型         | 一次（直线） | 二次（抛物线） | 分段一次 | 分段二次   |
| 代数精度         | 1            | 3              | —        | —          |
| 误差阶           | $O(h^3)$     | $O(h^5)$       | $O(h^2)$ | $O(h^4)$   |
| 收敛速度         | 慢           | 较快           | 中等     | 快         |
| 计算量（同等 n） | 小           | 小             | 中       | 中         |
| 同精度所需 n     | 很大         | 较大           | 较大     | 小         |
| 实用性           | 低           | 中             | 高       | 很高       |

**结论：**
1. 辛普森公式利用二次插值，拟合非线性曲线能力远优于梯形直线拟合。
2. 复化求积可以有效提升精度，减小截断误差，是工程实际中的主要手段。
3. 复化辛普森公式在同等计算量下精度最高，是工程数值积分的首选方法。
4. 数值积分算法具备良好的线性性、稳定性和收敛性，适配各类工程数值计算场景。
5. 机器学习拟合积分是新型数值求解思路，无需依赖传统插值细分迭代，在复杂非线性工程函数求解中具备高效、高精度的优势，但需防止过拟合，是传统数值积分方法的有效补充。

## 七、实验思考题

### 1. 为什么辛普森公式对三次多项式精确？

辛普森公式基于二次插值构建，代数精度本应为 2。但由于辛普森系数 $\frac{1}{6}, \frac{4}{6}, \frac{1}{6}$ 的特殊选取，三次多项式 $x^3$ 在 $[a,b]$ 上的积分恰好与辛普森近似值相等：

$$\int_a^b x^3 dx = \frac{b^4 - a^4}{4}, \quad S = \frac{b-a}{6}[a^3 + 4(\frac{a+b}{2})^3 + b^3]$$

两者相等可以验证。从代数角度看，辛普森公式关于中点对称，而 $x^3$ 的积分关于中点有特殊的对称性使得误差恰好为零。这使得辛普森公式的代数精度从 2 提升到 3。

### 2. 复化梯形和复化辛普森的误差阶为什么不同？

复化梯形在每个子区间上用一次插值，局部误差 $O(h^3)$，$n$ 个区间累加后全局误差为 $n \cdot O(h^3) = O(h^2)$。复化辛普森在每个双子区间上用二次插值，局部误差 $O(h^5)$，$n/2$ 个双子区间累加后全局误差为 $(n/2) \cdot O(h^5) = O(h^4)$。根本原因在于插值多项式次数不同，导致局部截断误差阶不同，累加后全局误差阶也不同。

### 3. 数值积分的线性性在工程计算中有什么意义？

工程中常需计算多个物理量叠加的积分，如合力做功 $W = \int (F_1 + F_2 + F_3) dx$。线性性使得我们可以分别计算 $\int F_i dx$ 再求和，简化了复杂问题的计算流程。此外，线性性还保证了数值积分算子的数学性质良好（有界性、稳定性等），使得误差分析更加简洁。

### 4. 机器学习拟合积分与传统复化积分相比，各有哪些工程优缺点？

**传统复化积分优点：** 理论完备，误差阶明确，稳定性好，适用于任意光滑函数。
**传统复化积分缺点：** 高精度需要大量节点，对非光滑函数效果差，需要手动选择步长。

**ML 拟合积分优点：** 可用较少采样点获得高精度，对采样点位置无严格等距要求，可自适应选择多项式阶数。
**ML 拟合积分缺点：** 高阶多项式可能过拟合（Runge 现象），理论误差分析不如传统方法完善，对噪声敏感。

### 5. 数值积分误差阶在工程精度把控中的作用？

误差阶直接给出了步长 $h$ 与误差之间的关系，使工程师能根据精度要求反推所需步长。例如，若工程要求误差 $< 10^{-6}$，复化辛普森误差 $O(h^4)$，则 $h^4 < 10^{-6}$，即 $h < 0.032$，$n > 32$。这种预判能力避免了盲目试算，提高了工程计算效率。

## 八、参考文献

[1] 李庆扬, 王能超, 易大义. 数值分析[M]. 5版. 北京: 清华大学出版社, 2018.

[2] 华东师范大学数学系. 数学分析[M]. 4版. 北京: 高等教育出版社, 2019.

[3] 张志涌. MATLAB数值计算与工程应用[M]. 北京: 北京航空航天大学出版社, 2020.

[4] 周志华. 机器学习[M]. 北京: 清华大学出版社, 2016.

[5] 王正林. 数值计算方法与工程实践[M]. 北京: 电子工业出版社, 2017.
