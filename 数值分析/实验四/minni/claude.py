import numpy as np

def f(t):
    """速度函数 v(t) = 4/(1+t^2)"""
    return 4 / (1 + t**2)

def trapezoidal_rule(a, b):
    """普通梯形公式，两点公式"""
    return (b - a) * (f(a) + f(b)) / 2

def simpson_rule(a, b):
    """普通辛普森公式，三点抛物线插值"""
    mid = (a + b) / 2
    return (b - a) / 6 * (f(a) + 4*f(mid) + f(b))

def composite_trapezoidal_rule(a, b, n):
    """复化梯形公式：间隔均匀 n 份"""
    h = (b - a) / n
    s = 0.5 * (f(a) + f(b))
    for i in range(1, n):
        s += f(a + i * h)
    return h * s

def composite_simpson_rule(a, b, n):
    """复化辛普森公式，n 必须为偶数"""
    if n % 2 != 0:
        raise ValueError("复化辛普森积分区间数 n 必须为偶数")
    h = (b - a) / n
    x = np.linspace(a, b, n + 1)
    s = f(a) + f(b)
    for i in range(1, n):
        coeff = 4 if i % 2 != 0 else 2
        s += coeff * f(x[i])
    return h * s / 3

def main():
    a, b = 0, 1
    exact = np.pi  # 理论积分值 ~3.141592653589793

    print("计算区间：[0, 1]")
    print("理论积分值 π = {:.8f}".format(exact))
    print()

    # 普通梯形
    trap = trapezoidal_rule(a, b)
    trap_err = abs(trap - exact)
    print("普通梯形公式积分结果: {:.8f}, 误差: {:.8e}".format(trap, trap_err))

    # 普通辛普森
    simp = simpson_rule(a, b)
    simp_err = abs(simp - exact)
    print("普通辛普森公式积分结果: {:.8f}, 误差: {:.8e}".format(simp, simp_err))
    
    # 复化公式，测试不同 n
    print("\n复化积分误差变化(n=2,4,8,16,32):")
    ns = [2, 4, 8, 16, 32]
    print("n\t复化梯形积分\t误差\t\t复化辛普森积分\t误差")
    for n in ns:
        comp_trap = composite_trapezoidal_rule(a, b, n)
        trap_err = abs(comp_trap - exact)
        comp_simp = composite_simpson_rule(a, b, n)
        simp_err = abs(comp_simp - exact)
        print(f"{n}\t{comp_trap:.8f}\t{trap_err:.2e}\t{comp_simp:.8f}\t{simp_err:.2e}")

if __name__ == "__main__":
    main()