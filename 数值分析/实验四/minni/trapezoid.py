import math


def v(t):
    return 4.0 / (1.0 + t * t)


EXACT = math.pi


def trapezoid_single(f, a, b):
    return (b - a) * (f(a) + f(b)) / 2.0


def composite_trapezoid(f, a, b, n):
    h = (b - a) / n
    total = 0.5 * (f(a) + f(b))

    for i in range(1, n):
        x_i = a + i * h
        total += f(x_i)

    return h * total


def main():
    a = 0.0
    b = 1.0

    print("精确值：")
    print(f"pi = {EXACT:.15f}")
    print()

    T = trapezoid_single(v, a, b)

    print("普通公式：")
    print(f"普通梯形公式结果：   {T:.15f}, 绝对误差：{abs(T - EXACT):.15e}")
    print()

    print("复化公式：")
    print(f"{'n':>6} | {'复化梯形结果':>12} | {'梯形误差':>10}")
    print("-" * 42)

    for n in [2, 4, 8, 16, 32, 64]:
        Tn = composite_trapezoid(v, a, b, n)

        print(
            f"{n:6d} | "
            f"{Tn:18.12f} | "
            f"{abs(Tn - EXACT):14.6e}"
        )


if __name__ == "__main__":
    main()
