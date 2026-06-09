import numpy as np
import matplotlib.pyplot as plt

def v(t):
    return 4.0 / (1.0 + t * t)

t = np.linspace(0, 1, 200)
y = v(t)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# ========== 左图：梯形公式 ==========
ax1.plot(t, y, linewidth=3, color='#1f77b4', label='真实曲线')

t_trap = np.array([0, 1])
y_trap = v(t_trap)
ax1.plot(t_trap, y_trap, linewidth=3, color='#ff7f0e', label='直线近似')

ax1.fill_between(t_trap, y_trap, color='#ffb888', alpha=0.6)
ax1.scatter(t_trap, y_trap, color='#ff7f0e', s=60, zorder=5)

ax1.set_xlim(0, 1)
ax1.set_ylim(0, 4.2)
ax1.set_xlabel('t')
ax1.set_ylabel('v(t)')
ax1.set_title('梯形公式：直线近似', fontsize=14)
ax1.grid(True, alpha=0.3, linestyle='--')
ax1.legend()

# ========== 右图：辛普森公式 ==========
ax2.plot(t, y, linewidth=3, color='#1f77b4', label='真实曲线')

t_simp = np.array([0, 0.5, 1])
y_simp = v(t_simp)

# 拟合抛物线
coeffs = np.polyfit(t_simp, y_simp, 2)
p = np.poly1d(coeffs)
t_parabola = np.linspace(0, 1, 200)
y_parabola = p(t_parabola)

ax2.plot(t_parabola, y_parabola, linewidth=3, color='#2ca02c', label='抛物线近似')
ax2.fill_between(t_parabola, y_parabola, color='#a8e6cf', alpha=0.6)
ax2.scatter(t_simp, y_simp, color='#2ca02c', s=60, zorder=5)

ax2.set_xlim(0, 1)
ax2.set_ylim(0, 4.2)
ax2.set_xlabel('t')
ax2.set_ylabel('v(t)')
ax2.set_title('辛普森公式：抛物线近似', fontsize=14)
ax2.grid(True, alpha=0.3, linestyle='--')
ax2.legend()

plt.tight_layout()
plt.savefig('积分公式近似图.png', dpi=300, bbox_inches='tight')
plt.show()
