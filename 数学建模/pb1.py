import numpy as np
import matplotlib.pyplot as plt
import matplotlib


# ============================================================
# 设置中文字体
# ============================================================
matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
matplotlib.rcParams['axes.unicode_minus'] = False

# ============================================================
# 一、资费函数定义
# ============================================================

def cost_standard(x, y, z=0):
    """
    现行全球通标准资费
    x: 本地主叫分钟数
    y: 本地被叫分钟数
    z: 长途分钟数（使用17951 IP）
    """
    return 50 + 0.40 * x + 0.40 * y + 0.70 * z


def cost_beijing(x, tier):
    """
    北京全球通畅听99套餐
    x: 本地主叫分钟数
    tier: 档位 (1, 2, 3, 4)
    注意：被叫免费，不消耗包含量
    """
    tiers = {
        1: {'M': 99,  'Q': 280,  'r': 0.35},
        2: {'M': 139, 'Q': 560,  'r': 0.25},
        3: {'M': 199, 'Q': 1000, 'r': 0.20},
        4: {'M': 299, 'Q': 2000, 'r': 0.15},
    }
    t = tiers[tier]
    overage = max(0, x - t['Q'])
    return t['M'] + t['r'] * overage


def cost_beijing_best(x):
    """
    北京畅听99套餐最优档位选择
    返回 (最优档位, 费用)
    """
    best_tier = 1
    best_cost = float('inf')
    for tier in [1, 2, 3, 4]:
        c = cost_beijing(x, tier)
        if c < best_cost:
            best_cost = c
            best_tier = tier
    return best_tier, best_cost


def cost_shanghai(x, y, tier):
    """
    上海移动全球通68套餐
    x: 本地主叫分钟数
    y: 本地被叫分钟数
    tier: 档位 (1, 2, 3)
    注意：包含量是主叫+被叫合计，被叫消耗包含量但不额外收费
    """
    tiers = {
        1: {'M': 68,  'Q': 360,  'r': 0.18},
        2: {'M': 128, 'Q': 800,  'r': 0.16},
        3: {'M': 188, 'Q': 1200, 'r': 0.13},
    }
    t = tiers[tier]
    # 被叫消耗后剩余的包含量给主叫
    remaining_for_call = max(0, t['Q'] - y)
    overage = max(0, x - remaining_for_call)
    return t['M'] + t['r'] * overage


def cost_shanghai_best(x, y):
    """
    上海68套餐最优档位选择
    返回 (最优档位, 费用)
    """
    best_tier = 1
    best_cost = float('inf')
    for tier in [1, 2, 3]:
        c = cost_shanghai(x, y, tier)
        if c < best_cost:
            best_cost = c
            best_tier = tier
    return best_tier, best_cost


# ============================================================
# 二、单点示例验证
# ============================================================

def demo_single_user():
    """单个典型用户的各种方案费用对比"""
    x, y, z = 400, 450, 30   # 中等用户
    alpha = y / x if x > 0 else 0

    print("=" * 60)
    print(f"典型用户: 主叫 x={x}, 被叫 y={y}, 长途 z={z}, α={alpha:.2f}")
    print("=" * 60)

    c_std = cost_standard(x, y, z)
    print(f"标准资费:               {c_std:.2f} 元")

    tier_bj, c_bj = cost_beijing_best(x)
    print(f"北京畅听99 (档{tier_bj}):        {c_bj:.2f} 元")

    tier_sh, c_sh = cost_shanghai_best(x, y)
    print(f"上海68套餐 (档{tier_sh}):        {c_sh:.2f} 元")

    print()


# ============================================================
# 三、盈亏平衡分析
# ============================================================

def find_breakeven_std_vs_bj(alpha=1.0):
    """
    寻找标准资费与北京畅听99档1的盈亏平衡点
    C_std = 50 + 0.40*(1+alpha)*x
    C_bj1 = 99 (当 x <= 280) 或 99 + 0.35*(x-280) (当 x > 280)
    """
    print(f"\n{'='*60}")
    print(f"盈亏平衡分析: 标准资费 vs 北京畅听99档1 (α={alpha})")
    print(f"{'='*60}")

    # 情况1: x <= 280
    # 50 + 0.40*(1+alpha)*x = 99
    if alpha > -1:
        x1 = 49 / (0.40 * (1 + alpha))
        if 0 < x1 <= 280:
            print(f"情况1 (x≤280): 平衡点 x* = {x1:.1f} 分钟")
            print(f"  x < {x1:.1f} → 标准资费更优")
            print(f"  {x1:.1f} ≤ x ≤ 280 → 畅听99档1更优")
        else:
            print(f"情况1 (x≤280): 平衡点 x* = {x1:.1f} 分钟 (不在[0,280]区间)")

    # 情况2: x > 280
    # 99 + 0.35*(x-280) = 50 + 0.40*(1+alpha)*x
    # 1 + 0.35x = 50 + 0.40*(1+alpha)*x
    # 0.35x - 0.40*(1+alpha)*x = 49
    # x*(0.35 - 0.40 - 0.40*alpha) = 49
    # x*(-0.05 - 0.40*alpha) = 49
    denom = -0.05 - 0.40 * alpha
    if abs(denom) > 1e-10:
        x2 = 49 / denom
        if x2 > 280:
            print(f"情况2 (x>280): 平衡点 x* = {x2:.1f} 分钟")
        else:
            print(f"情况2 (x>280): 无有效平衡点 (x*={x2:.1f} ≤ 280)")
            print(f"  → 畅听99档1在x>280时永远优于标准资费")
    else:
        print("情况2: 分母为零，无解")

    print()


def find_breakeven_bj_tiers():
    """寻找北京畅听99各档位之间的切换点"""
    print(f"{'='*60}")
    print("北京畅听99档间切换点")
    print(f"{'='*60}")

    # 档1→档2: 99 + 0.35*(x-280) = 139 (x>280)
    x12 = 280 + (139 - 99) / 0.35
    print(f"档1 → 档2: x* = {x12:.1f} 分钟")

    # 档2→档3: 139 + 0.25*(x-560) = 199 (x>560)
    x23 = 560 + (199 - 139) / 0.25
    print(f"档2 → 档3: x* = {x23:.1f} 分钟")

    # 档3→档4: 199 + 0.20*(x-1000) = 299 (x>1000)
    x34 = 1000 + (299 - 199) / 0.20
    print(f"档3 → 档4: x* = {x34:.1f} 分钟")

    print()
    return x12, x23, x34


def find_breakeven_std_vs_sh(alpha=1.0):
    """寻找标准资费与上海68档1的盈亏平衡点"""
    print(f"{'='*60}")
    print(f"盈亏平衡分析: 标准资费 vs 上海68档1 (α={alpha})")
    print(f"{'='*60}")

    # 当x+y <= 360 (即 (1+alpha)*x <= 360)
    # 50 + 0.40*(1+alpha)*x = 68
    x_crit = 360 / (1 + alpha)  # 总通话量恰好等于包含量的临界x
    x1 = 18 / (0.40 * (1 + alpha))

    print(f"  总通话量恰好360分钟时的主叫量: x = {x_crit:.1f}")
    print(f"  平衡点: x* = {x1:.1f} 分钟")
    if x1 <= x_crit:
        print(f"  x < {x1:.1f} → 标准资费更优")
        print(f"  {x1:.1f} ≤ x ≤ {x_crit:.1f} → 上海68档1更优")
    print()


# ============================================================
# 四、最优方案判定
# ============================================================

def find_optimal_plan(x, y, z=0):
    """
    对于给定的(x, y, z)，判定四个方案中哪个最优
    返回 (方案名, 档位, 费用)
    """
    plans = {}

    # 标准资费
    plans['标准资费'] = ('-', cost_standard(x, y, z))

    # 北京畅听99
    tier_bj, c_bj = cost_beijing_best(x)
    plans['北京畅听99'] = (f'档{tier_bj}', c_bj)

    # 上海68套餐
    tier_sh, c_sh = cost_shanghai_best(x, y)
    plans['上海68套餐'] = (f'档{tier_sh}', c_sh)

    # 被叫全免费计划
    c_mf = 50 + 0.40 * x + 0.70 * z
    plans['被叫全免费'] = ('-', c_mf)

    # 找最优
    best_plan = min(plans, key=lambda k: plans[k][1])
    return best_plan, plans


def classify_users():
    """对不同类型的用户进行分类，给出推荐方案"""
    print(f"\n{'='*60}")
    print("用户分类与推荐方案")
    print(f"{'='*60}")

    user_types = [
        ("U1 极低", 30, 50, 5, 20),
        ("U2 低", 80, 120, 10, 50),
        ("U3 中低", 200, 250, 20, 80),
        ("U4 中等", 400, 450, 30, 100),
        ("U5 中高", 800, 600, 50, 150),
        ("U6 高", 1500, 1000, 80, 200),
    ]

    print(f"{'类型':<10} {'主叫':<6} {'被叫':<6} {'最优方案':<12} {'费用(元)':<10} {'对手费用':<10}")
    print("-" * 60)

    for name, x, y, z, s in user_types:
        best, plans = find_optimal_plan(x, y, z)
        c_best = plans[best][1]
        # 第二便宜的费用
        sorted_plans = sorted(plans.items(), key=lambda kv: kv[1][1])
        second_name = sorted_plans[1][0]
        second_cost = sorted_plans[1][1][1]
        print(f"{name:<10} {x:<6} {y:<6} {best:<12} {c_best:<10.1f} {second_name}: {second_cost:<8.1f}")

    print()


# ============================================================
# 五、可视化
# ============================================================

def plot_cost_comparison(alpha=1.0, x_max=1500):
    """
    绘制各方案费用随主叫量x变化的曲线
    alpha: 被叫/主叫比例
    """
    x_vals = np.linspace(0, x_max, 500)

    c_std = [cost_standard(x, alpha*x) for x in x_vals]
    c_bj_best = [cost_beijing_best(x)[1] for x in x_vals]
    c_sh_best = [cost_shanghai_best(x, alpha*x)[1] for x in x_vals]
    c_mf = [50 + 0.40*x for x in x_vals]

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(x_vals, c_std, 'k-', linewidth=2, label='标准资费 (双向收费)')
    ax.plot(x_vals, c_bj_best, 'b-', linewidth=2, label='北京畅听99 (最优档)')
    ax.plot(x_vals, c_sh_best, 'r--', linewidth=2, label='上海68套餐 (最优档)')
    ax.plot(x_vals, c_mf, 'g-.', linewidth=2, label='被叫全免费计划')
    ax.set_xlabel('月主叫分钟数 x', fontsize=12)
    ax.set_ylabel('月费用 (元)', fontsize=12)
    ax.set_title(f'各方案费用对比 (α={alpha})', fontsize=13)
    ax.legend(fontsize=10, loc='upper left')
    ax.set_xlim([0, x_max])
    ax.set_ylim([0, 600])
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('cost_comparison.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("图表已保存为 cost_comparison.png")


# ============================================================
# 六、生成费用对照表
# ============================================================

def print_cost_table(x_values, alpha=1.0):
    """打印完整的费用对照表"""
    print(f"\n{'='*80}")
    print(f"费用对照表 (α={alpha})")
    print(f"{'='*80}")
    header = f"{'主叫x':<8} {'标准':<10} {'全免费':<10} {'BJ档1':<10} {'BJ档2':<10} {'BJ档3':<10} {'BJ档4':<10} {'SH档1':<10} {'SH档2':<10} {'SH档3':<10} {'最优':<12}"
    print(header)
    print("-" * len(header))

    for x in x_values:
        y = alpha * x
        std = cost_standard(x, y)
        mf = 50 + 0.40 * x
        bj1 = cost_beijing(x, 1)
        bj2 = cost_beijing(x, 2)
        bj3 = cost_beijing(x, 3)
        bj4 = cost_beijing(x, 4)
        sh1 = cost_shanghai(x, y, 1)
        sh2 = cost_shanghai(x, y, 2)
        sh3 = cost_shanghai(x, y, 3)
        all_costs = {'标准': std, '全免费': mf,
                     'BJ档1': bj1, 'BJ档2': bj2, 'BJ档3': bj3, 'BJ档4': bj4,
                     'SH档1': sh1, 'SH档2': sh2, 'SH档3': sh3}
        best = min(all_costs, key=all_costs.get)

        print(f"{x:<8} {std:<10.1f} {mf:<10.1f} {bj1:<10.1f} {bj2:<10.1f} "
              f"{bj3:<10.1f} {bj4:<10.1f} {sh1:<10.1f} {sh2:<10.1f} {sh3:<10.1f} {best:<12}")
    print()


# ============================================================
# 主程序
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("2007数学建模C题 问题一：资费计算与用户适用性分析")
    print("=" * 60)

    # 1. 单个用户示例
    demo_single_user()

    # 2. 盈亏平衡分析
    for alpha in [0, 0.5, 1.0, 1.5, 2.0]:
        find_breakeven_std_vs_bj(alpha)
    find_breakeven_bj_tiers()
    find_breakeven_std_vs_sh(alpha=1.0)

    # 3. 用户分类
    classify_users()

    # 4. 打印费用表（α=1，主被叫相等）
    x_test = [50, 100, 150, 180, 200, 250, 280, 300, 350, 394, 400, 450,
              560, 600, 700, 800, 900, 1000, 1200, 1500, 1800, 2000, 2500, 3000]
    print_cost_table(x_test, alpha=1.0)

    # 5. 打印费用表（α=0，纯主叫）
    print_cost_table(x_test, alpha=0.0)

    # 6. 可视化
    plot_cost_comparison(alpha=1.0, x_max=1500)

    print("\n分析完成！")