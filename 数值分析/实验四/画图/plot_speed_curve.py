import numpy as np
import matplotlib.pyplot as plt

def v(t):
    return 4.0 / (1.0 + t * t)

t = np.linspace(0, 1, 200)
y = v(t)

fig, ax = plt.subplots(figsize=(9, 5))

ax.plot(t, y, linewidth=3, color='#1f77b4', label=r'$v(t) = \frac{4}{1+t^2}$')

t_fill = np.linspace(0, 1, 200)
y_fill = v(t_fill)
ax.fill_between(t_fill, y_fill, color='#aed6f1', alpha=0.7)

ax.scatter([0.5, 1], [v(0.5), v(1)], color='#f39c12', s=60, zorder=5)

ax.text(0.6, 1.5, r'$S = \int_0^1 \frac{4}{1+t^2} dt = \pi$', fontsize=20)

ax.set_xlim(0, 1)
ax.set_ylim(0, 4.2)
ax.set_xlabel('时间 t / s')
ax.set_title('速度曲线与位移面积', fontsize=16)
ax.grid(True, alpha=0.3, linestyle='--')
ax.legend()

plt.tight_layout()
plt.savefig('速度曲线与位移面积.png', dpi=300, bbox_inches='tight')
plt.show()
