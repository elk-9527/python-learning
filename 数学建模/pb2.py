"问题二：手机套餐资费计算与用户适用性分析"
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
matplotlib.rcParams['axes.unicode_minus'] = False

# ====================================================
# 复用问题一的资费函数
# ====================================================
def cost_standard(x, y):
    return 50 + 0.40 * x + 0.40 * y

def cost_beijing(x, tier):
    T = {1: (99, 280, 0.35), 2: (139, 560, 0.25),
         3: (199, 1000, 0.20), 4: (299, 2000, 0.15)}
    M, Q, r = T[tier]
    return M + r * max(0, x - Q)

def beijing_best(x):
    best = min((cost_beijing(x, t), t) for t in range(1, 5))
    return best[1], best[0]  # tier, cost

def cost_shanghai(x, y, tier):
    T = {1: (68, 360, 0.18), 2: (128, 800, 0.16), 3: (188, 1200, 0.13)}
    M, Q, r = T[tier]
    remaining = max(0, Q - y)
    return M + r * max(0, x - remaining)

def shanghai_best(x, y):
    best = min((cost_shanghai(x, y, t), t) for t in range(1, 4))
    return best[1], best[0]  # tier, cost

def cost_free(x, y):
    return 50 + 0.40 * x  # 被叫免费计划

# ====================================================
# 6类典型用户
# ====================================================
users = {
    'U1': (30, 50, 0.15),   # (主叫, 被叫, 人群占比)
    'U2': (80, 120, 0.25),
    'U3': (200, 250, 0.25),
    'U4': (400, 450, 0.18),
    'U5': (800, 600, 0.12),
    'U6': (1500, 1000, 0.05),
}

# 4个方案名
plan_names = ['标准资费', '北京畅听99', '上海68套餐', '被叫全免费']

# ====================================================
# 对给定用户计算4个方案的基础数据
# 返回: [(费用, 边际成本, 最低月付, 所选档位), ...]
# ====================================================
def calc_plan_info(x, y):
    info = []

    # A1: 标准
    c = cost_standard(x, y)
    info.append({'cost': c, 'marginal': 0.40, 'min_pay': 50, 'tier': '-'})

    # A2: 北京畅听99
    tier, c = beijing_best(x)
    r = {1: 0.35, 2: 0.25, 3: 0.20, 4: 0.15}[tier]
    M = {1: 99, 2: 139, 3: 199, 4: 299}[tier]
    info.append({'cost': c, 'marginal': r, 'min_pay': M, 'tier': tier})

    # A3: 上海68
    tier, c = shanghai_best(x, y)
    r = {1: 0.18, 2: 0.16, 3: 0.13}[tier]
    M = {1: 68, 2: 128, 3: 188}[tier]
    info.append({'cost': c, 'marginal': r, 'min_pay': M, 'tier': tier})

    # A4: 被叫全免费
    c = cost_free(x, y)
    info.append({'cost': c, 'marginal': 0.40, 'min_pay': 50, 'tier': '-'})

    return info

# ====================================================
# 方案的"全局指标"（不随用户类型变化）
# C5: 对U1收费, C6: 对U6收费, C7: 6类用户费用标准差
# C8-C15: 方案固有属性
# ====================================================
# 先算每个方案对6类用户的费用（用于C5, C6, C7）
all_user_costs = {}  # plan_idx -> [6类用户的费用]
for pi in range(4):
    costs = []
    for uk, (x, y, _) in users.items():
        infos = calc_plan_info(x, y)
        costs.append(infos[pi]['cost'])
    all_user_costs[pi] = costs

# C5: 对U1的费用（取U1的cost）
# C6: 对U6的费用
# C7: 6类用户费用的标准差
def get_c5(pi):
    return all_user_costs[pi][0]  # U1

def get_c6(pi):
    return all_user_costs[pi][5]  # U6

def get_c7(pi):
    return np.std(all_user_costs[pi])

# C8-C15: 方案固有属性（手动设定）
# 格式: [标准资费, 北京畅听99, 上海68, 被叫全免费]
C8_params  = [2, 3, 3, 2]       # 计费参数个数
C9_hidden  = [0, 1, 1, 1]       # 有隐藏条款=1
C10_tiers  = [1, 4, 3, 1]       # 可选档位数
C11_data   = [0, 1, 0, 0]       # 可叠加数据=1
C12_contract=[0, 0, 0, 1]       # 需签约=1
C13_gprs   = [0, 10, 0, 0]      # 赠送GPRS(MB)，北京取最低档
C14_sms    = [0, 0, 0, 0]       # 赠送短信，都差不多
C15_free   = [0, 1, 1, 1]       # 被叫免费=1

# ====================================================
# 构建某类用户的决策矩阵 (4方案 x 15指标)
# 指标全部是"原始值"（还没正向化）
# 返回 numpy array, shape (4, 15)
# ====================================================
def build_matrix(x, y):
    infos = calc_plan_info(x, y)
    total = x + y
    m = np.zeros((4, 15))

    for pi in range(4):
        info = infos[pi]

        # C1: 月均支出（元）
        m[pi, 0] = info['cost']
        # C2: 单位分钟成本（元/分钟）
        m[pi, 1] = info['cost'] / total if total > 0 else 999
        # C3: 边际成本（元/分钟）
        m[pi, 2] = info['marginal']
        # C4: 最低月付（元）
        m[pi, 3] = info['min_pay']
        # C5: 低用量负担（U1费用）
        m[pi, 4] = get_c5(pi)
        # C6: 高用量负担（U6费用）
        m[pi, 5] = get_c6(pi)
        # C7: 价格离散度（6类用户费用标准差）
        m[pi, 6] = get_c7(pi)
        # C8: 计费参数个数
        m[pi, 7] = C8_params[pi]
        # C9: 隐藏条款
        m[pi, 8] = C9_hidden[pi]
        # C10: 可选档位数
        m[pi, 9] = C10_tiers[pi]
        # C11: 可叠加数据
        m[pi, 10] = C11_data[pi]
        # C12: 需签约
        m[pi, 11] = C12_contract[pi]
        # C13: 赠送GPRS
        m[pi, 12] = C13_gprs[pi]
        # C14: 赠送短信
        m[pi, 13] = C14_sms[pi]
        # C15: 免费被叫
        m[pi, 14] = C15_free[pi]

    return m

# ====================================================
# 指标方向: 1=越大越好(正向), 0=越小越好(负向)
# ====================================================
indicator_direction = [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1]
# C1-C9: 越小越好; C10-C11: 越大越好; C12: 越小越好; C13-C15: 越大越好

indicator_names = [
    '月均支出', '单位分钟成本', '边际成本', '最低月付',
    '低用量负担', '高用量负担', '价格离散度', '计费参数个数',
    '隐藏条款', '可选档位数', '可叠加数据', '需签约',
    '赠送数据', '赠送短信', '免费被叫'
]

# ====================================================
# 正向化 + 归一化
# ====================================================
def normalize_matrix(raw):
    """正向化后做向量归一化，返回 (归一化矩阵, 正向化矩阵)"""
    m, n = raw.shape
    forward = np.zeros_like(raw)

    for j in range(n):
        col = raw[:, j]
        if indicator_direction[j] == 1:
            # 已经正向
            forward[:, j] = col
        else:
            # 极小型 -> 极大型: a' = max - a
            forward[:, j] = np.max(col) - col

    # 向量归一化
    col_norms = np.sqrt(np.sum(forward**2, axis=0))
    col_norms[col_norms == 0] = 1e-10
    normed = forward / col_norms

    return normed, forward

# ====================================================
# 熵权法
# ====================================================
def entropy_weight(normed):
    """输入归一化矩阵，返回权重向量"""
    m, n = normed.shape
    # 平移保证正值（用于计算比重）
    shifted = normed + 1e-10

    # 比重 p_ij
    p = shifted / np.sum(shifted, axis=0, keepdims=True)

    # 信息熵
    k = 1.0 / np.log(m)
    e = -k * np.sum(p * np.log(p), axis=0)

    # 差异系数
    d = 1 - e

    # 权重
    w = d / np.sum(d)
    return w

# ====================================================
# TOPSIS
# ====================================================
def topsis(normed, w):
    """返回每个方案的相对贴近度"""
    m, n = normed.shape
    # 加权矩阵
    v = normed * w

    # 正负理想解
    v_pos = np.max(v, axis=0)
    v_neg = np.min(v, axis=0)

    # 距离
    d_pos = np.sqrt(np.sum((v - v_pos)**2, axis=1))
    d_neg = np.sqrt(np.sum((v - v_neg)**2, axis=1))

    # 相对贴近度
    c = d_neg / (d_pos + d_neg + 1e-10)
    return c

# ====================================================
# 主流程：对每类用户做TOPSIS，然后按人群占比加权
# ====================================================
print("=" * 60)
print("问题二：熵权-TOPSIS 资费方案评价")
print("=" * 60)

all_scores = {}   # user_key -> [4个方案的C_i]
all_weights = {}  # user_key -> 权重向量

for uk, (x, y, ratio) in users.items():
    raw = build_matrix(x, y)
    normed, forward = normalize_matrix(raw)
    w = entropy_weight(normed)
    scores = topsis(normed, w)

    all_scores[uk] = scores
    all_weights[uk] = w

    print(f"\n--- {uk} (主叫{x}, 被叫{y}, 占比{ratio*100:.0f}%) ---")
    print(f"  各方案TOPSIS得分:")
    for pi, name in enumerate(plan_names):
        marker = " ★" if scores[pi] == max(scores) else ""
        print(f"    {name}: {scores[pi]:.4f}{marker}")

# 加权综合
print("\n" + "=" * 60)
print("按人群占比加权综合结果")
print("=" * 60)

weighted = np.zeros(4)
for uk, (x, y, ratio) in users.items():
    weighted += all_scores[uk] * ratio

ranking = sorted(zip(plan_names, weighted), key=lambda kv: -kv[1])
for rank, (name, score) in enumerate(ranking, 1):
    print(f"  {rank}. {name}: {score:.4f}")

# 平均权重
print("\n各指标平均权重（熵权法得出）:")
avg_w = np.mean(list(all_weights.values()), axis=0)
# 按权重大小排序输出
sorted_idx = np.argsort(-avg_w)
for i in sorted_idx:
    print(f"  {indicator_names[i]:<14s}: {avg_w[i]:.4f}")

# ====================================================
# 画一个简单的图：加权综合得分
# ====================================================
fig, ax = plt.subplots(figsize=(8, 4))
colors = ['#c44', '#4a90d9', '#e05252', '#50b86c']
bars = ax.barh(plan_names, weighted, color=colors, edgecolor='white', height=0.5)
for bar, val in zip(bars, weighted):
    ax.text(bar.get_width() + 0.01, bar.get_y() + bar.get_height()/2,
            f'{val:.3f}', va='center', fontsize=11)

ax.set_xlim([0, 1.0])
ax.set_xlabel('综合得分 (越高越优)', fontsize=11)
ax.set_title('各资费方案综合评价结果 (熵权-TOPSIS)', fontsize=13)
ax.invert_yaxis()
plt.tight_layout()
plt.savefig('eval_result.png', dpi=150, bbox_inches='tight')
plt.show()
print("\n图已保存 eval_result.png")