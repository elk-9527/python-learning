"""
2007数学建模C题 - 问题三：评价"被叫全免费计划"

方案：月租50，被叫免费，主叫0.40/分钟，其他同标准资费，至少绑一年。
需要回答：这个方案怎么样？为什么？
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
    """标准资费：月租50 + 双向0.40"""
    return 50 + 0.40 * x + 0.40 * y


def cost_free(x):
    """被叫全免费：月租50 + 主叫0.40 + 被叫免费"""
    return 50 + 0.40 * x


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


def cost_sh(x, y, tier):
    """上海68套餐"""
    T = {1: (68, 360, 0.18), 2: (128, 800, 0.16), 3: (188, 1200, 0.13)}
    M, Q, r = T[tier]
    remaining = max(0, Q - y)
    return M + r * max(0, x - remaining)


def sh_best(x, y):
    """上海68最优档"""
    best = min(((cost_sh(x, y, t), t) for t in range(1, 4)), key=lambda v: v[0])
    return best[1], best[0]


# ============================================================
# 第一部分：盈亏平衡 —— 全免费和其它方案比，谁在什么情况下更优
# ============================================================

def breakeven():
    print("=" * 56)
    print("一、盈亏平衡分析")
    print("=" * 56)

    # ---- 1. vs 标准资费 ----
    print("\n1. 全免费 vs 标准资费")
    print("   " + "-" * 40)
    print("   标准:   50 + 0.40(x+y)")
    print("   全免费: 50 + 0.40x")
    print("   节省 = 0.40y")
    print("   只要 y>0，全免费就严格优于标准资费。")
    print("   这是帕累托改进——没人多付钱，接电话的人省了。")

    # ---- 2. vs 畅听99档1 ----
    print("\n2. 全免费 vs 畅听99档1 (99元/280分钟/超出0.35)")
    print("   " + "-" * 40)

    # x <= 280 段
    x_switch1 = (99 - 50) / 0.40  # = 122.5
    print(f"   区间 x ≤ 280:")
    print(f"     50 + 0.40x = 99  =>  x* = {x_switch1:.1f}")
    print(f"     x < {x_switch1:.1f}  → 全免费更优")
    print(f"     {x_switch1:.1f} ≤ x ≤ 280 → 畅听99档1更优")

    # x > 280 段
    # 全免费 = 50+0.40x, 档1 = 99+0.35(x-280) = 1+0.35x
    # 差 = 49+0.05x > 0 恒成立 → 档1永远更优
    print(f"   区间 x > 280:")
    print(f"     全免费: 50 + 0.40x")
    print(f"     档1:    1 + 0.35x  (化简后)")
    print(f"     差值 = 49 + 0.05x > 0 恒成立")
    print(f"     → 畅听99档1永远更优")

    # ---- 3. vs 畅听99档2 ----
    print("\n3. 全免费 vs 畅听99档2 (139元/560分钟/超出0.25)")
    print("   " + "-" * 40)
    x_switch2 = (139 - 50) / 0.40  # = 222.5
    print(f"   区间 x ≤ 560:")
    print(f"     50 + 0.40x = 139  =>  x* = {x_switch2:.1f}")
    print(f"     x < {x_switch2:.1f}  → 全免费更优")
    print(f"     {x_switch2:.1f} ≤ x ≤ 560 → 畅听99档2更优")
    print(f"   区间 x > 560:")
    print(f"     全免费: 50+0.40x,  档2: -1+0.25x")
    print(f"     差值 = 51+0.15x > 0 → 档2永远更优")

    # ---- 4. vs 上海68档1 ----
    print("\n4. 全免费 vs 上海68档1 (68元/360分钟总通话/超出0.18)")
    print("   " + "-" * 40)
    print("   设 α=1 (主被叫相等), 总通话 T=2x")
    print("   当 T≤360 (x≤180): 上海档1=68, 全免费=50+0.40x")
    x_sh1 = (68 - 50) / 0.40  # = 45
    print(f"     50+0.40x = 68  =>  x* = {x_sh1:.0f}")
    print(f"     x < {x_sh1:.0f} → 全免费更优")
    print(f"     {x_sh1:.0f} ≤ x ≤ 180 → 上海68档1更优")

    # 当 x>180 时，上海档1费用更高，但仍有其它档
    print(f"   区间 x > 180:")
    print(f"     上海档1开始超额计费，全免费可能反超")
    print(f"     需具体计算（参见后文数值比较）")

    # ---- 5. 汇总 ----
    print("\n5. 最优方案区间汇总 (α=1, 仅本地通话)")
    print("   " + "-" * 40)
    bj_switch_12 = 394   # 档1→档2
    bj_switch_23 = 800   # 档2→档3
    bj_switch_34 = 1500  # 档3→档4

    rows = [
        (f"< {x_sh1:.0f}", "全免费", "通话极少"),
        (f"{x_sh1:.0f} ~ {x_switch1:.0f}", "全免费 / 上海68档1", "需具体比较"),
        (f"{x_switch1:.0f} ~ 394", "畅听99档1", "被叫免费+280分钟打出"),
        ("394 ~ 800", "畅听99档2", "主叫量大升级档位"),
        ("800 ~ 1500", "畅听99档3", ""),
        ("> 1500", "畅听99档4", ""),
    ]
    print(f"    {'主叫量x':<18} {'最优':<18} {'备注'}")
    for rng, best, note in rows:
        print(f"    {rng:<18} {best:<18} {note}")

    print(f"\n   关键结论：")
    print(f"   全免费只在 x < {x_switch1:.0f} 时比畅听99档1有优势。")
    print(f"   主叫量稍大一点，套餐的低单价优势就盖过全免费的50元低月租。")


# ============================================================
# 第二部分：数值对比表 —— 直观看各种用户各方案花多少钱
# ============================================================

def numeric_compare():
    print("\n" + "=" * 56)
    print("二、数值对比 (α=1, 主被叫相等)")
    print("=" * 56)

    xs = [30, 50, 80, 100, 122, 150, 200, 250, 300, 400, 500, 600, 800, 1000]

    header = f"  {'x':<6} {'标准':<8} {'全免费':<8} {'BJ档1':<8} {'BJ档2':<8} {'SH档1':<8} {'SH档2':<8} {'最优':<10}"
    print(header)
    print("  " + "-" * len(header))

    for x in xs:
        y = x  # α=1
        std = cost_standard(x, y)
        free = cost_free(x)
        bj1 = cost_bj(x, 1)
        bj2 = cost_bj(x, 2)
        sh1 = cost_sh(x, y, 1)
        sh2 = cost_sh(x, y, 2)

        all_c = {'标准': std, '全免费': free, 'BJ1': bj1,
                 'BJ2': bj2, 'SH1': sh1, 'SH2': sh2}
        best = min(all_c, key=all_c.get)

        print(f"  {x:<6} {std:<8.0f} {free:<8.0f} {bj1:<8.0f} "
              f"{bj2:<8.0f} {sh1:<8.0f} {sh2:<8.0f} {best:<10}")

    # 关键观察
    print(f"\n  观察：")
    print(f"  - x=30~50:  全免费最便宜（比标准省了被叫费，又没到套餐门槛）")
    print(f"  - x=80~100: 上海68档1反超全免费（总通话还在360分钟内）")
    print(f"  - x=122:    全免费和畅听99档1打平")
    print(f"  - x≥150:    套餐全面优于全免费")


# ============================================================
# 第三部分：长途资费差异
# ============================================================

def longdistance_note():
    print("\n" + "=" * 56)
    print("三、长途资费差异（容易被忽略的细节）")
    print("=" * 56)
    print("""
  题目说全免费"其他项目资费均同现行的资费标准"。
  这意味着长途、漫游、短信都和标准资费一样。

  但北京畅听99套餐有一条关键优惠：
  "17951国内IP长途资费 0.10元/分钟"

  对比：
    全免费打长途: 0.40(区内) + 0.30(IP) = 0.70元/分钟
    畅听99打长途: 0.10(IP) + 主叫分钟从包含量扣或按超出算
                   = 0.10元/分钟（长途部分）
                  （区内部分含在主叫里，套餐已覆盖或按超出费率算）

  也就是说：畅听99的长途IP费只要0.10，而全免费要0.30。
  对于每月打30分钟长途的用户：
    全免费长途费: 30×0.70 = 21元
    畅听99长途费: 30×0.10 =  3元（区内部分另算，但通常被套餐包含）
  每月差18元，一年差216元。

  这是全免费计划另一个隐性劣势。
""")


# ============================================================
# 第四部分：捆绑约束的期权分析
# ============================================================

def option_analysis():
    print("=" * 56)
    print("四、捆绑约束的期权分析（\"至少在网一年\"值多少钱）")
    print("=" * 56)

    # 设定：用户当前月主叫80分钟，有一定概率涨到350分钟
    x_now = 80
    x_up = 350
    p_up = 0.35  # 通话量上升的概率

    # 各方案月费
    free_now = cost_free(x_now)    # 50+0.4*80 = 82
    free_up  = cost_free(x_up)     # 50+0.4*350 = 190

    bj1_now  = cost_bj(x_now, 1)   # 80≤280 → 99
    bj1_up   = cost_bj(x_up, 1)    # 350→99+0.35*(350-280)=123.5

    print(f"""
  情景设定：
    用户当前主叫 {x_now} 分钟/月
    未来可能升至 {x_up} 分钟/月（概率 {p_up}）
    假设前6个月通话量不变，后6个月可能变化（简化模型）

  各方案月费：
    全免费: {x_now}分钟→{free_now:.0f}元, {x_up}分钟→{free_up:.0f}元
    畅听99档1: {x_now}分钟→{bj1_now:.0f}元, {x_up}分钟→{bj1_up:.1f}元
""")

    # 情况A：签全免费（锁一年）
    # 前6月x_now，后6月x_up（如果上升）或x_now（如果不升）
    cost_A_up = 6 * free_now + 6 * free_up
    cost_A_stay = 12 * free_now
    cost_A_exp = p_up * cost_A_up + (1 - p_up) * cost_A_stay

    # 情况B：不签约，选畅听99档1（随时可换档）
    cost_B_up = 6 * bj1_now + 6 * bj1_up
    cost_B_stay = 12 * bj1_now
    cost_B_exp = p_up * cost_B_up + (1 - p_up) * cost_B_stay

    # 情况C：灵活策略——前6月用畅听99档1，
    #        后6月如果通话量涨了就升档2，不涨继续档1
    bj2_up = cost_bj(x_up, 2)  # 350≤560→139
    cost_C_up = 6 * bj1_now + 6 * bj2_up
    cost_C_stay = 12 * bj1_now
    cost_C_exp = p_up * cost_C_up + (1 - p_up) * cost_C_stay

    print(f"  三种策略的年费用期望：")
    print(f"    A. 签全免费（锁一年）:    {cost_A_exp:.0f} 元")
    print(f"    B. 不签，选畅听99档1:     {cost_B_exp:.0f} 元")
    print(f"    C. 不签，灵活升档 (1→2):   {cost_C_exp:.0f} 元")
    print(f"")
    print(f"    全免费 vs 畅听99档1:  {'全免费省' if cost_A_exp < cost_B_exp else '畅听99省'} {abs(cost_A_exp - cost_B_exp):.0f} 元")
    print(f"    全免费 vs 灵活策略:   {'全免费省' if cost_A_exp < cost_C_exp else '灵活策略省'} {abs(cost_A_exp - cost_C_exp):.0f} 元")

    # 期权价值
    option_value = cost_A_exp - cost_C_exp
    if option_value > 0:
        print(f'\n    被剥夺的"切换权"价值 ≈ {option_value:.0f} 元/年')
        print(f"    等于签约全免费比灵活策略多付的钱。")
    else:
        print(f"\n    在本组参数下，签约全免费期望更省。")
        print(f"    但若通话量涨幅更大或概率更高，结论会翻转。")

    # 敏感性：不同涨幅下的期权价值
    print(f"\n  敏感性测试（不同未来通话量下的期权价值）:")
    print(f"    {'未来x':<8} {'全免费月费':<12} {'畅听99档1':<12} {'期权价值/年':<14}")
    for x_test in [150, 250, 350, 500, 700]:
        free_test = cost_free(x_test)
        bj1_test = cost_bj(x_test, 1)
        # 期权价值 = 后6个月全免费超额支出 * p_up
        ov = p_up * max(0, free_test - bj1_test) * 6
        print(f"    {x_test:<8} {free_test:<12.0f} {bj1_test:<12.1f} {ov:<14.0f}")

    print(f"\n  结论：通话量涨得越多，被锁在全免费里的代价越大。")
    print(f"  运营商用\"在网一年\"锁住用户，就是为了防止低端用户")
    print(f"  通话量增长后流向高性价比套餐。")


# ============================================================
# 第五部分：图 —— 费用曲线 + 优势区间
# ============================================================

def plot_analysis():
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    x = np.linspace(0, 600, 300)

    # 左：各方案费用曲线
    ax = axes[0]
    ax.plot(x, cost_standard(x, x), 'gray', lw=2, label='标准资费 (α=1)')
    ax.plot(x, cost_free(x), 'g-', lw=2.5, label='被叫全免费')
    ax.plot(x, [cost_bj(xi, 1) for xi in x], 'b--', lw=1.8, label='畅听99档1')
    ax.plot(x, [cost_bj(xi, 2) for xi in x], 'r--', lw=1.8, label='畅听99档2')
    ax.plot(x, [cost_sh(xi, xi, 1) for xi in x], 'orange', ls='-.', lw=1.6, label='上海68档1')

    # 标注切换点
    for xp, label in [(122.5, '122.5'), (222.5, '222.5')]:
        ax.axvline(x=xp, color='gray', ls=':', alpha=0.4)
        ax.text(xp + 5, 30, label, fontsize=8, color='gray')

    ax.set_xlim([0, 600])
    ax.set_ylim([0, 350])
    ax.set_xlabel('月主叫 x (分钟)', fontsize=11)
    ax.set_ylabel('月费用 (元)', fontsize=11)
    ax.set_title('各方案费用曲线 (α=1)', fontsize=12)
    ax.legend(fontsize=7.5, loc='upper left')
    ax.grid(True, alpha=0.2)

    # 右：全免费 vs 畅听99档1 差值
    ax = axes[1]
    diff = np.array([cost_free(xi) - cost_bj(xi, 1) for xi in x])
    ax.fill_between(x, diff, 0, where=(diff < 0),
                    color='green', alpha=0.2, label='全免费更优')
    ax.fill_between(x, diff, 0, where=(diff > 0),
                    color='blue', alpha=0.2, label='畅听99更优')
    ax.plot(x, diff, 'k-', lw=1.5)
    ax.axhline(y=0, color='gray', ls='-', alpha=0.5)
    ax.axvline(x=122.5, color='red', ls='--', alpha=0.5, label='x=122.5')
    ax.set_xlim([0, 600])
    ax.set_xlabel('月主叫 x (分钟)', fontsize=11)
    ax.set_ylabel('全免费 - 畅听99档1 (元)', fontsize=11)
    ax.set_title('费用差：全免费 minus 畅听99档1', fontsize=12)
    ax.legend(fontsize=8, loc='upper left')
    ax.grid(True, alpha=0.2)

    plt.tight_layout()
    plt.savefig('q3_analysis.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("\n图已保存 q3_analysis.png")


# ============================================================
# 运行
# ============================================================
if __name__ == "__main__":
    breakeven()
    numeric_compare()
    longdistance_note()
    option_analysis()
    plot_analysis()

    print("\n" + "=" * 56)
    print("综合评价总结")
    print("=" * 56)
    print("""
  优点：
    - 规则极简：50元月租 + 0.40主叫 + 被叫免费，用户一看就懂
    - 月租低（50元)，对通话量很少的用户友好
    - 被叫免费是实质性进步（相比标准资费的双向收费）
    - 是单向收费的制度性突破

  缺点：
    - 主叫0.40元/分钟太贵，套餐超出费率普遍在0.15-0.25
    - 无增值服务（不送流量、短信）
    - 长途资费和标准一样（IP 0.30/分钟），而畅听99只要0.10
    - 捆绑一年——用户失去切换套餐的灵活性

  适合人群：
    月主叫 < 122分钟、以接听为主、不常打长途的用户。
    典型画像：退休老人、备用机、偶尔用手机的人。

  策略本质：
    这是移动公司的"筛选"手段——用低月租+高单价吸引低端用户，
    同时用套餐（高月租+低单价）留住中高端用户。
    捆绑条款防止低端用户通话量增长后立刻逃走。
""")