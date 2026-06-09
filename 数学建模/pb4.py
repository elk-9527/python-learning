"""
2007数学建模C题 - 问题四：设计新资费方案

约束：收入降幅 ≤ 10%
目标：用户月费尽量低
方法：对数正态分布模拟用户 -> 随机搜索套餐参数 -> 蒙特卡洛评估
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib

matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
matplotlib.rcParams['axes.unicode_minus'] = False

# ============================================================
# 资费函数
# ============================================================

def cost_standard(x, y):
    """标准资费"""
    return 50 + 0.40 * x + 0.40 * y


def cost_bj(x, tier):
    """北京畅听99"""
    T = {
        1: (99, 280, 0.35),
        2: (139, 560, 0.25),
        3: (199, 1000, 0.20),
        4: (299, 2000, 0.15),
    }
    M, Q, r = T[tier]
    return M + r * max(0, x - Q)


def bj_best(x):
    """畅听99最优档，返回 (档位, 费用)"""
    best = min(((cost_bj(x, t), t) for t in range(1, 5)), key=lambda v: v[0])
    return best[1], best[0]


def cost_new(x, tier, params):
    """
    新方案资费
    params = [(M1, Q1, r1), (M2, Q2, r2), ...]
    tier: 0-based 档位索引
    """
    M, Q, r = params[tier]
    return M + r * max(0, x - Q)


def new_best(x, params):
    """新方案最优档，返回 (档位索引, 费用)"""
    n = len(params)
    best = min(((cost_new(x, t, params), t) for t in range(n)), key=lambda v: v[0])
    return best[1], best[0]


# ============================================================
# 用户生成
# ============================================================

def generate_users(n=8000, mu=4.5, sigma=0.85, alpha_mu=0.15, alpha_sigma=0.4, seed=42):
    """
    生成 n 个模拟用户
    x ~ lognormal(mu, sigma)  主叫量
    alpha ~ lognormal(alpha_mu, alpha_sigma)  接听比 y/x

    返回 x, y 数组
    """
    rng = np.random.default_rng(seed)
    x = rng.lognormal(mean=mu, sigma=sigma, size=n)
    alpha = rng.lognormal(mean=alpha_mu, sigma=alpha_sigma, size=n)
    y = alpha * x
    return x, y


def user_stats(x, y):
    """打印用户分布概况"""
    print(f"  用户数: {len(x)}")
    print(f"  主叫x: 均值={np.mean(x):.0f}, 中位数={np.median(x):.0f}, "
          f"P10={np.percentile(x, 10):.0f}, P90={np.percentile(x, 90):.0f}")
    print(f"  被叫y: 均值={np.mean(y):.0f}, 中位数={np.median(y):.0f}")
    print(f"  接听比α: 均值={np.mean(y/x):.2f}, 中位数={np.median(y/x):.2f}")


# ============================================================
# 评估函数
# ============================================================

def evaluate(params, x, y):
    """
    params: 档位参数列表 [(M1,Q1,r1), (M2,Q2,r2), ...]
    x, y: 用户通话量数组

    返回 dict:
      revenue:     平均每用户运营商收入
      avg_cost:    平均每用户支出
      adoption:    选择新方案的比例（而非标准资费）
      tier_dist:   各档选择比例 [标准, 档1, 档2, ...]
      dominated:   是否有档位无人选
    """
    n_users = len(x)
    n_tiers = len(params)

    M = np.array([p[0] for p in params])
    Q = np.array([p[1] for p in params])
    r = np.array([p[2] for p in params])

    excess = np.maximum(0, x - Q[:, np.newaxis])
    costs_new_all = M[:, np.newaxis] + r[:, np.newaxis] * excess

    tiers = np.argmin(costs_new_all, axis=0)
    costs_new = np.min(costs_new_all, axis=0)
    costs_std = 50 + 0.40 * x + 0.40 * y

    choose_new = costs_new < costs_std
    actual_cost = np.where(choose_new, costs_new, costs_std)

    revenue = np.mean(actual_cost)
    adoption = np.mean(choose_new)

    tier_idx = np.where(choose_new, tiers + 1, 0)
    tier_dist = np.bincount(tier_idx, minlength=n_tiers + 1).astype(float) / n_users

    tier_usage = np.bincount(tiers[choose_new], minlength=n_tiers)
    dominated = np.any(tier_usage == 0)

    return {
        'revenue': revenue,
        'avg_cost': revenue,
        'adoption': adoption,
        'tier_dist': tier_dist,
        'dominated': dominated,
    }


# ============================================================
# 基准：北京畅听99
# ============================================================

def evaluate_baseline(x, y):
    """计算畅听99作为基准时的指标"""
    M = np.array([99, 139, 199, 299])
    Q = np.array([280, 560, 1000, 2000])
    r_arr = np.array([0.35, 0.25, 0.20, 0.15])

    excess = np.maximum(0, x - Q[:, np.newaxis])
    costs_bj_all = M[:, np.newaxis] + r_arr[:, np.newaxis] * excess

    costs_bj = np.min(costs_bj_all, axis=0)
    costs_std = 50 + 0.40 * x + 0.40 * y

    choose_bj = costs_bj < costs_std
    actual_cost = np.where(choose_bj, costs_bj, costs_std)
    revenue = np.mean(actual_cost)
    adoption = np.mean(choose_bj)

    return revenue, adoption


# ============================================================
# 参数搜索
# ============================================================

def random_params(n_candidates=200, n_tiers=3, seed=123):
    """
    随机生成候选参数，保证单调性
    M递增, Q递增, r递减
    """
    rng = np.random.default_rng(seed)
    candidates = []

    # 不同档位数用不同的搜索范围
    if n_tiers == 3:
        M_ranges = [(45, 90), (90, 180), (160, 320)]
        Q_ranges = [(120, 350), (350, 900), (900, 2800)]
        r_ranges = [(0.20, 0.40), (0.12, 0.28), (0.06, 0.20)]
    elif n_tiers == 4:
        M_ranges = [(40, 80), (80, 140), (140, 220), (220, 350)]
        Q_ranges = [(100, 300), (300, 650), (650, 1200), (1200, 3000)]
        r_ranges = [(0.22, 0.42), (0.15, 0.30), (0.10, 0.22), (0.06, 0.16)]
    else:
        # 通用
        M_ranges = [(40 + i*40, 80 + i*60) for i in range(n_tiers)]
        Q_ranges = [(80 + i*100, 300 + i*400) for i in range(n_tiers)]
        r_ranges = [(0.08 + 0.04*(n_tiers-i), 0.16 + 0.06*(n_tiers-i)) for i in range(n_tiers)]

    max_attempts = n_candidates * 5
    for _ in range(max_attempts):
        M = np.sort(rng.uniform(20, 350, size=n_tiers))
        Q = np.sort(rng.uniform(80, 3000, size=n_tiers))
        r = -np.sort(-rng.uniform(0.04, 0.45, size=n_tiers))

        # 裁剪到合理范围
        for i in range(n_tiers):
            lo, hi = M_ranges[i]
            M[i] = np.clip(M[i], lo, hi)
            lo, hi = Q_ranges[i]
            Q[i] = np.clip(Q[i], lo, hi)
            lo, hi = r_ranges[i]
            r[i] = np.clip(r[i], lo, hi)

        # 检查单调性
        ok = True
        for i in range(n_tiers - 1):
            if M[i] >= M[i+1] or Q[i] >= Q[i+1] or r[i] <= r[i+1]:
                ok = False
                break
        if not ok:
            continue

        # 档位间距不能太小
        if n_tiers >= 2:
            if M[1] - M[0] < 8:
                continue
        if n_tiers >= 3:
            if M[2] - M[1] < 15:
                continue
            if Q[1] - Q[0] < 40:
                continue
            if r[0] - r[1] < 0.015:
                continue
        if n_tiers >= 4:
            if M[3] - M[2] < 20:
                continue
            if Q[2] - Q[1] < 60:
                continue

        params = [(M[i], Q[i], r[i]) for i in range(n_tiers)]
        candidates.append(params)

        if len(candidates) >= n_candidates:
            break

    return candidates


def search_best(x, y, baseline_revenue, candidates):
    """
    在候选参数中搜索最优方案
    约束: revenue >= 0.9 * baseline_revenue
    目标: min avg_cost
    """
    best_params = None
    best_result = None

    for params in candidates:
        res = evaluate(params, x, y)

        if res['revenue'] < 0.9 * baseline_revenue:
            continue
        if res['dominated']:
            continue
        if res['adoption'] < 0.5:
            continue

        if best_result is None or res['avg_cost'] < best_result['avg_cost']:
            best_params = params
            best_result = res

    if best_params is None:
        return None, None

    info = {
        'params': best_params,
        'revenue': best_result['revenue'],
        'avg_cost': best_result['avg_cost'],
        'adoption': best_result['adoption'],
        'tier_dist': best_result['tier_dist'],
        'revenue_change': (best_result['revenue'] - baseline_revenue) / baseline_revenue * 100,
    }
    return best_params, info


# ============================================================
# 手动候选方案
# ============================================================

def manual_candidates():
    """手动设计的候选方案"""
    cand = []

    # 候选1：之前分析中推荐的 3 档
    cand.append([(58, 200, 0.25), (118, 600, 0.18), (198, 1500, 0.12)])

    # 候选2：更低门槛 3 档
    cand.append([(48, 150, 0.30), (108, 550, 0.20), (188, 1400, 0.13)])

    # 候选3：偏高端 3 档
    cand.append([(68, 250, 0.22), (138, 650, 0.16), (228, 1800, 0.10)])

    # 候选4：四档方案
    cand.append([(48, 150, 0.30), (98, 400, 0.22),
                 (168, 900, 0.15), (268, 2000, 0.10)])

    # 候选5：3 档
    cand.append([(55, 180, 0.28), (115, 580, 0.18), (195, 1600, 0.11)])

    return cand


def evaluate_manual(x, y, baseline_revenue):
    """评估手动候选方案"""
    print("\n" + "-" * 60)
    print("手动候选方案评估")
    print("-" * 60)

    manuals = manual_candidates()
    for idx, params in enumerate(manuals):
        n_tiers = len(params)
        res = evaluate(params, x, y)
        rev_chg = (res['revenue'] - baseline_revenue) / baseline_revenue * 100

        ok = res['revenue'] >= 0.9 * baseline_revenue and not res['dominated']
        status = "[OK] 可行" if ok else "[X] 不可行"
        print(f"\n  候选{idx+1} ({n_tiers}档) {status}")
        for t, (M, Q, r) in enumerate(params):
            print(f"    档{t+1}: 月费{M:.0f}元  含{Q:.0f}分钟  超出{r:.2f}元/分")
        print(f"    收入/用户={res['revenue']:.1f} ({rev_chg:+.1f}%)  "
              f"选择率={res['adoption']:.1%}")
        if res['dominated']:
            print(f"    !! 有档位无人选")


# ============================================================
# 灵敏度分析
# ============================================================

def sensitivity(best_params, x, y, baseline_revenue):
    """对最优方案的关键参数做扰动分析"""
    print("\n" + "=" * 56)
    print("灵敏度分析（收入变化%）")
    print("=" * 56)

    base_res = evaluate(best_params, x, y)
    base_rev = base_res['revenue']
    n_tiers = len(best_params)

    # 真正改变分布均值的用户生成函数
    def users_mean_up():
        return generate_users(5000, mu=4.6, seed=200)  # mean up ~10%

    def users_mean_down():
        return generate_users(5000, mu=4.4, seed=201)  # mean down ~10%

    tests = [
        ("用户通话量整体 +~10%", users_mean_up),
        ("用户通话量整体 -~10%", users_mean_down),
        (f"档1月费 M1 +8元", None, 'M1_up'),
        (f"档1月费 M1 -8元", None, 'M1_down'),
        (f"档{n_tiers}超出费率 r +0.03", None, 'r_up'),
        (f"档{n_tiers}超出费率 r -0.03", None, 'r_down'),
        ("档1包含量 Q1 +40分钟", None, 'Q1_up'),
        ("档1包含量 Q1 -40分钟", None, 'Q1_down'),
    ]

    print(f"  {'扰动因素':<34} {'收入/用户':<12} {'变化':<10}")
    print(f"  {'-'*34} {'-'*12} {'-'*10}")
    print(f"  {'基准（无扰动）':<34} {base_rev:<12.1f} {'--':<10}")

    for item in tests:
        if len(item) == 2:
            name, user_fn = item
            x2, y2 = user_fn()
            res = evaluate(best_params, x2, y2)
        else:
            name, _, tag = item
            # 复制参数并扰动
            p = [list(t) for t in best_params]  # mutable copy
            if tag == 'M1_up':
                p[0][0] += 8
            elif tag == 'M1_down':
                p[0][0] = max(25, p[0][0] - 8)
            elif tag == 'r_up':
                p[-1][2] = min(0.40, p[-1][2] + 0.03)
            elif tag == 'r_down':
                p[-1][2] = max(0.04, p[-1][2] - 0.03)
            elif tag == 'Q1_up':
                p[0][1] += 40
            elif tag == 'Q1_down':
                p[0][1] = max(50, p[0][1] - 40)
            # 转回 tuple
            p = [tuple(t) for t in p]
            res = evaluate(p, x, y)

        chg = (res['revenue'] - base_rev) / base_rev * 100
        print(f"  {name:<34} {res['revenue']:<12.1f} {chg:+.1f}%")


# ============================================================
# 画图
# ============================================================

def plot_result(best_params, x, y, baseline_revenue):
    """对比图：新方案 vs 畅听99 费用曲线 + 用户费用变化"""
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))

    # 左：费用曲线
    ax = axes[0]
    x_curve = np.linspace(10, 2500, 400)

    bj_curve = np.array([bj_best(xi)[1] for xi in x_curve])
    ax.plot(x_curve, bj_curve, 'b-', lw=2, alpha=0.7, label='畅听99 (现有)')

    new_curve = np.array([new_best(xi, best_params)[1] for xi in x_curve])
    ax.plot(x_curve, new_curve, 'r-', lw=2.5, label='新方案')

    std_curve = np.array([cost_standard(xi, 1.2 * xi) for xi in x_curve])
    ax.plot(x_curve, std_curve, 'gray', lw=1.5, alpha=0.5, label='标准资费 (α=1.2)')

    # 标注新方案各档包含量
    for _, Q, _ in best_params:
        ax.axvline(x=Q, color='red', ls=':', alpha=0.3)

    ax.set_xlim([0, 2500])
    ax.set_ylim([0, 500])
    ax.set_xlabel('月主叫 x (分钟)', fontsize=11)
    ax.set_ylabel('月费用 (元)', fontsize=11)
    ax.set_title('费用曲线对比', fontsize=12)
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.2)

    # 右：用户费用变化分布
    ax = axes[1]
    n_sample = min(2000, len(x))
    rng = np.random.default_rng(0)
    idx = rng.choice(len(x), n_sample, replace=False)
    x_sample = x[idx]
    y_sample = y[idx]

    actual_new = np.zeros(n_sample)
    actual_bj = np.zeros(n_sample)

    for i in range(n_sample):
        std_c = cost_standard(x_sample[i], y_sample[i])
        _, bj_c = bj_best(x_sample[i])
        _, new_c = new_best(x_sample[i], best_params)
        actual_bj[i] = min(bj_c, std_c)
        actual_new[i] = min(new_c, std_c)

    diff = actual_new - actual_bj
    ax.hist(diff, bins=50, color='steelblue', edgecolor='white', alpha=0.8)
    ax.axvline(x=0, color='black', ls='-', lw=1)
    ax.axvline(x=np.mean(diff), color='red', ls='--', lw=1.5,
               label=f'均值: {np.mean(diff):+.1f}元')
    ax.set_xlabel('新方案月费 - 畅听99月费 (元)', fontsize=11)
    ax.set_ylabel('用户数', fontsize=11)
    ax.set_title('每用户月费变化分布', fontsize=12)
    ax.legend(fontsize=9)

    plt.tight_layout()
    plt.savefig('q4_result.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("图已保存 q4_result.png")


# ============================================================
# 输出最优方案详情
# ============================================================

def print_best(info, baseline_revenue, baseline_adoption):
    """格式化输出最优方案"""
    params = info['params']
    n_tiers = len(params)
    print("\n" + "=" * 56)
    print(f"最优方案 ({n_tiers}档)")
    print("=" * 56)
    for t, (M, Q, r) in enumerate(params):
        print(f"  档{t+1}: 月费 {M:.0f}元  |  含 {Q:.0f}分钟主叫  "
              f"|  超出 {r:.2f}元/分  |  被叫免费")
    print(f"\n  预期收入/用户: {info['revenue']:.1f} 元/月  "
          f"(畅听99基准: {baseline_revenue:.1f}, 变化: {info['revenue_change']:+.1f}%)")
    print(f"  用户月均支出:   {info['avg_cost']:.1f} 元")
    print(f"  选择率:         {info['adoption']:.1%}  "
          f"(畅听99: {baseline_adoption:.1%})")
    print(f"  收入约束下限:   {0.9*baseline_revenue:.1f} 元/月  "
          f"{'[OK] 满足' if info['revenue'] >= 0.9*baseline_revenue else '[X] 不满足'}")

    # 档位分布
    td = info['tier_dist']
    dist_str = f"标准资费: {td[0]:.1%}"
    for t in range(n_tiers):
        dist_str += f",  档{t+1}: {td[t+1]:.1%}"
    print(f"  档位分布:       {dist_str}")

    # 与畅听99逐项对比
    print(f"\n  与畅听99对比:")
    print(f"    入门档月费:    畅听99 = 99元  ->  新方案 = {params[0][0]:.0f}元")
    print(f"    最低超出费率:  畅听99 = 0.15  ->  新方案 = {params[-1][2]:.2f}")
    print(f"    档位数:        畅听99 = 4档   ->  新方案 = {n_tiers}档")


# ============================================================
# 主程序
# ============================================================

if __name__ == "__main__":
    print("=" * 56)
    print("问题四：新资费方案设计")
    print("=" * 56)

    # 1. 生成用户
    print("\n[1] 生成模拟用户...")
    x, y = generate_users(8000, mu=4.5, sigma=0.85, seed=42)
    user_stats(x, y)

    # 2. 基准评估
    print("\n[2] 计算基准（北京畅听99）...")
    base_rev, base_adopt = evaluate_baseline(x, y)
    print(f"  基准收入/用户: {base_rev:.1f} 元/月")
    print(f"  套餐选择率:    {base_adopt:.1%}")
    print(f"  收入约束下限:  {0.9 * base_rev:.1f} 元/月")

    # 3. 随机搜索（3档 + 4档分别搜）
    print("\n[3] 随机搜索候选参数...")
    rand_3 = random_params(n_candidates=300, n_tiers=3, seed=7)
    rand_4 = random_params(n_candidates=200, n_tiers=4, seed=13)
    all_rand = rand_3 + rand_4
    print(f"  3档候选: {len(rand_3)} 组,  4档候选: {len(rand_4)} 组")
    print(f"  共 {len(all_rand)} 组候选参数")

    # 4. 搜索最优
    print("\n[4] 搜索最优方案...")
    best, info = search_best(x, y, base_rev, all_rand)

    # 5. 和手动候选比较
    print("\n[5] 与手动候选方案比较...")
    manuals = manual_candidates()
    for params in manuals:
        res = evaluate(params, x, y)
        ok = (res['revenue'] >= 0.9 * base_rev and
              not res['dominated'] and
              res['adoption'] >= 0.5)
        if ok:
            if best is None or res['avg_cost'] < info['avg_cost']:
                best = params
                info = {
                    'params': best,
                    'revenue': res['revenue'],
                    'avg_cost': res['avg_cost'],
                    'adoption': res['adoption'],
                    'tier_dist': res['tier_dist'],
                    'revenue_change': (res['revenue'] - base_rev) / base_rev * 100,
                }

    # 6. 兜底
    if best is None:
        print("\n!! 未找到完全满足约束的方案，使用默认推荐。")
        best = [(58, 200, 0.25), (118, 600, 0.18), (198, 1500, 0.12)]
        res = evaluate(best, x, y)
        info = {
            'params': best,
            'revenue': res['revenue'],
            'avg_cost': res['avg_cost'],
            'adoption': res['adoption'],
            'tier_dist': res['tier_dist'],
            'revenue_change': (res['revenue'] - base_rev) / base_rev * 100,
        }

    # 7. 输出
    print_best(info, base_rev, base_adopt)
    evaluate_manual(x, y, base_rev)

    # 8. 灵敏度
    sensitivity(best, x, y, base_rev)

    # 9. 画图
    plot_result(best, x, y, base_rev)

    print("\n分析完成。")