import math


def v(t):
    return 4.0 / (1.0 + t * t)


EXACT = math.pi


def trapezoid_single(f, a, b):
    return (b - a) * (f(a) + f(b)) / 2.0


def simpson_single(f, a, b):
    m = (a + b) / 2.0
    return (b - a) * (f(a) + 4.0 * f(m) + f(b)) / 6.0


def composite_trapezoid(f, a, b, n):
    h = (b - a) / n
    total = 0.5 * (f(a) + f(b))

    for i in range(1, n):
        x_i = a + i * h
        total += f(x_i)

    return h * total


def composite_simpson(f, a, b, n):
    if n % 2 != 0:
        raise ValueError("复化辛普森公式要求 n 必须为偶数。")

    h = (b - a) / n

    odd_sum = 0.0
    even_sum = 0.0

    for i in range(1, n):
        x_i = a + i * h

        if i % 2 == 1:
            odd_sum += f(x_i)
        else:
            even_sum += f(x_i)

    return h / 3.0 * (f(a) + f(b) + 4.0 * odd_sum + 2.0 * even_sum)

def plot_error_step_and_cost():
    """
    绘制：
    1. 误差-步长图：观察 h=1/n 减小时误差变化；
    2. 误差-计算量图：对比四种算法的精度和计算量。
    """
    import matplotlib.pyplot as plt

    # 设置中文字体，避免中文乱码
    plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
    plt.rcParams["axes.unicode_minus"] = False
    plt.rcParams["mathtext.fontset"] = "dejavusans"

    a = 0.0
    b = 1.0

    # 复化公式使用的等分数
    ns = [2, 4, 8, 16, 32, 64]

    # 步长 h = (b-a)/n，本题为 h=1/n
    hs = [(b - a) / n for n in ns]

    # 普通公式误差
    T_single = trapezoid_single(v, a, b)
    S_single = simpson_single(v, a, b)

    err_T_single = abs(T_single - EXACT)
    err_S_single = abs(S_single - EXACT)

    # 复化公式误差
    trap_errors = []
    simp_errors = []

    for n in ns:
        Tn = composite_trapezoid(v, a, b, n)
        Sn = composite_simpson(v, a, b, n)

        trap_errors.append(abs(Tn - EXACT))
        simp_errors.append(abs(Sn - EXACT))

    # 计算量：函数调用点数
    # 普通梯形：2 个函数值
    # 普通辛普森：3 个函数值
    # 复化梯形、复化辛普森：n+1 个节点函数值
    cost_trap_single = 2
    cost_simp_single = 3
    costs_composite = [n + 1 for n in ns]

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # =========================
    # 图 1：误差-步长图
    # =========================
    ax1 = axes[0]

    ax1.loglog(hs, trap_errors, "o-", linewidth=2, markersize=6, label="复化梯形公式")
    ax1.loglog(hs, simp_errors, "s-", linewidth=2, markersize=6, label="复化辛普森公式")

    # 普通公式误差不随 n 变化，用水平线表示
    ax1.hlines(
        err_T_single,
        min(hs),
        max(hs),
        colors="red",
        linestyles="--",
        linewidth=1.8,
        label="普通梯形误差"
    )

    ax1.hlines(
        err_S_single,
        min(hs),
        max(hs),
        colors="green",
        linestyles="--",
        linewidth=1.8,
        label="普通辛普森误差"
    )

    # 参考收敛阶曲线
    # 复化梯形理论为 O(h^2)
    ref_trap = [trap_errors[0] * (h / hs[0]) ** 2 for h in hs]

    # 复化辛普森一般为 O(h^4)，但本题实际表现为 O(h^6)
    ref_simp_4 = [simp_errors[0] * (h / hs[0]) ** 4 for h in hs]
    ref_simp_6 = [simp_errors[0] * (h / hs[0]) ** 6 for h in hs]

    ax1.loglog(hs, ref_trap, "k--", alpha=0.5, linewidth=1.5, label="$O(h^2)$ 参考线")
    ax1.loglog(hs, ref_simp_4, "gray", linestyle=":", alpha=0.8, linewidth=1.5, label="$O(h^4)$ 参考线")
    ax1.loglog(hs, ref_simp_6, "b--", alpha=0.4, linewidth=1.5, label="本题 $O(h^6)$ 参考线")

    ax1.set_xlabel("步长 h = 1/n（向右表示步长减小）")
    ax1.set_ylabel("绝对误差")
    ax1.set_title("误差-步长图")
    ax1.grid(True, which="both", linestyle="--", alpha=0.4)
    ax1.legend(fontsize=9)

    # 让横坐标从 h=1/2 到 h=1/64，向右表示 h 变小
    ax1.invert_xaxis()

    # =========================
    # 图 2：误差-计算量图
    # =========================
    ax2 = axes[1]

    # 普通公式是单点
    ax2.loglog(
        cost_trap_single,
        err_T_single,
        "ro",
        markersize=8,
        label="普通梯形公式"
    )

    ax2.loglog(
        cost_simp_single,
        err_S_single,
        "go",
        markersize=8,
        label="普通辛普森公式"
    )

    # 复化公式曲线
    ax2.loglog(
        costs_composite,
        trap_errors,
        "o-",
        linewidth=2,
        markersize=6,
        label="复化梯形公式"
    )

    ax2.loglog(
        costs_composite,
        simp_errors,
        "s-",
        linewidth=2,
        markersize=6,
        label="复化辛普森公式"
    )

    # 标注部分 n 值
    for cost, err, n in zip(costs_composite, trap_errors, ns):
        ax2.annotate(f"n={n}", (cost, err), textcoords="offset points", xytext=(5, 5), fontsize=8)

    ax2.set_xlabel("函数计算次数 / 节点数")
    ax2.set_ylabel("绝对误差")
    ax2.set_title("误差-计算量对比图")
    ax2.grid(True, which="both", linestyle="--", alpha=0.4)
    ax2.legend(fontsize=9)

    plt.tight_layout()

    # 保存图片
    plt.savefig("误差步长与计算量对比图.png", dpi=300, bbox_inches="tight")

    # 显示图片
    plt.show()

def main():
    a = 0.0
    b = 1.0

    print("精确值：")
    print(f"pi = {EXACT:.15f}")
    print()

    T = trapezoid_single(v, a, b)
    S = simpson_single(v, a, b)

    print("普通公式：")
    print(f"普通梯形公式结果：   {T:.15f}, 绝对误差：{abs(T - EXACT):.15e}")
    print(f"普通辛普森公式结果： {S:.15f}, 绝对误差：{abs(S - EXACT):.15e}")
    print()

    print("复化公式：")
    print(f"{'n':>6} | {'复化梯形结果':>12} | {'梯形误差':>10} | {'复化辛普森结果':>11} | {'辛普森误差':>8}")
    print("-" * 86)

    for n in [2, 4, 8, 16, 32, 64]:
        Tn = composite_trapezoid(v, a, b, n)
        Sn = composite_simpson(v, a, b, n)

        print(
            f"{n:6d} | "
            f"{Tn:18.12f} | "
            f"{abs(Tn - EXACT):14.6e} | "
            f"{Sn:18.12f} | "
            f"{abs(Sn - EXACT):14.6e}"
        )


if __name__ == "__main__":
    main()
    plot_error_step_and_cost()