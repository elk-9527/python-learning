import matplotlib.pyplot as plt
import numpy as np

# 数据来自终端输出
methods = ['普通梯形', '普通辛普森', '复化梯形\nn=16', '复化辛普森\nn=4']
errors = [0.1415926535897931, 0.008259320256459812, 0.0006510415, 0.00002402614]

colors = ['#e74c3c', '#2ecc71', '#3498db', '#e67e22']

fig, ax = plt.subplots(figsize=(10, 5))
bars = ax.bar(methods, errors, color=colors, width=0.6)

ax.set_yscale('log')
ax.set_ylim(2e-5, 2e-1)
ax.set_ylabel('绝对误差')
ax.set_title('代表性算法误差对比', fontsize=14)
ax.grid(True, axis='y', alpha=0.3, linestyle='--')

# 在柱子上标注数值
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height * 1.1,
            f'{height:.2e}', ha='center', va='bottom', fontsize=10)

plt.tight_layout()
plt.savefig('代表性算法误差对比.png', dpi=300, bbox_inches='tight')
plt.close()
