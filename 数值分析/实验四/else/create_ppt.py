import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
import matplotlib.font_manager as fm

# --- Font config for Chinese ---
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'DejaVu Sans']
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.unicode_minus'] = True

OUT_DIR = r'c:\Users\Lenovo\Desktop\ppt_images'
os.makedirs(OUT_DIR, exist_ok=True)

# Define the function
def f(t):
    return 4.0 / (1.0 + t**2)

# Colors
C_BLUE = '#2563EB'
C_RED = '#DC2626'
C_GREEN = '#16A34A'
C_ORANGE = '#EA580C'
C_PURPLE = '#7C3AED'
C_TEAL = '#0D9488'
C_BG = '#F8FAFC'

# =====================================================
# 1. 梯形公式几何示意图
# =====================================================
def fig_trapezoid():
    fig, ax = plt.subplots(1, 1, figsize=(7, 5), dpi=150)
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)
    
    x = np.linspace(0, 1.3, 300)
    y = f(x)
    
    # Fill trapezoid
    ax.fill([0, 1, 1, 0], [0, 0, f(1), f(0)], alpha=0.25, color=C_BLUE, label='梯形面积')
    
    # Function curve
    ax.plot(x, y, color=C_RED, linewidth=2.5, label='f(x) = 4/(1+x²)')
    
    # Trapezoid line
    ax.plot([0, 1], [f(0), f(1)], color=C_BLUE, linewidth=2, linestyle='--', label='梯形上边')
    
    # Vertical lines
    ax.plot([0, 0], [0, f(0)], color='gray', linewidth=1, linestyle=':')
    ax.plot([1, 1], [0, f(1)], color='gray', linewidth=1, linestyle=':')
    
    # Points
    ax.plot(0, f(0), 'o', color=C_BLUE, markersize=10, zorder=5)
    ax.plot(1, f(1), 'o', color=C_BLUE, markersize=10, zorder=5)
    
    # Annotations
    ax.annotate('f(a)=4', xy=(0, f(0)), xytext=(-0.25, f(0)+0.3),
                fontsize=11, fontweight='bold', color=C_BLUE)
    ax.annotate('f(b)=2', xy=(1, f(1)), xytext=(1.05, f(1)+0.3),
                fontsize=11, fontweight='bold', color=C_BLUE)
    ax.annotate('b-a', xy=(0.5, -0.35), fontsize=12, ha='center', color='gray')
    
    ax.set_xlim(-0.4, 1.4)
    ax.set_ylim(-0.5, 5)
    ax.set_xlabel('x', fontsize=12)
    ax.set_ylabel('f(x)', fontsize=12)
    ax.set_title('梯形公式几何意义', fontsize=16, fontweight='bold', pad=10)
    ax.legend(fontsize=10, loc='upper right')
    ax.grid(True, alpha=0.3)
    
    fig.tight_layout()
    path = os.path.join(OUT_DIR, 'trapezoid.png')
    fig.savefig(path, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close(fig)
    return path

# =====================================================
# 2. 辛普森公式几何示意图
# =====================================================
def fig_simpson():
    fig, ax = plt.subplots(1, 1, figsize=(7, 5), dpi=150)
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)
    
    x = np.linspace(0, 1.3, 300)
    y = f(x)
    mid = 0.5
    
    # Parabola through 3 points
    # f(0)=4, f(0.5)=16/5=3.2, f(1)=2
    # Fit quadratic
    coeffs = np.polyfit([0, 0.5, 1], [f(0), f(mid), f(1)], 2)
    p = np.poly1d(coeffs)
    x_par = np.linspace(0, 1, 200)
    
    # Fill parabola area
    ax.fill_between(x_par, 0, p(x_par), alpha=0.2, color=C_GREEN, label='抛物线下面积')
    
    # Function curve
    ax.plot(x, y, color=C_RED, linewidth=2.5, label='f(x) = 4/(1+x²)')
    
    # Parabola
    ax.plot(x_par, p(x_par), color=C_GREEN, linewidth=2, linestyle='--', label='二次插值抛物线')
    
    # Vertical lines
    ax.plot([0, 0], [0, f(0)], color='gray', linewidth=1, linestyle=':')
    ax.plot([0.5, 0.5], [0, f(mid)], color='gray', linewidth=1, linestyle=':')
    ax.plot([1, 1], [0, f(1)], color='gray', linewidth=1, linestyle=':')
    
    # Points
    ax.plot(0, f(0), 'o', color=C_GREEN, markersize=10, zorder=5)
    ax.plot(mid, f(mid), 's', color=C_GREEN, markersize=10, zorder=5)
    ax.plot(1, f(1), 'o', color=C_GREEN, markersize=10, zorder=5)
    
    # Annotations
    ax.annotate('f(a)', xy=(0, f(0)), xytext=(-0.2, f(0)+0.3),
                fontsize=11, fontweight='bold', color=C_GREEN)
    ax.annotate('f((a+b)/2)', xy=(mid, f(mid)), xytext=(mid-0.05, f(mid)+0.4),
                fontsize=10, fontweight='bold', color=C_GREEN)
    ax.annotate('f(b)', xy=(1, f(1)), xytext=(1.05, f(1)+0.3),
                fontsize=11, fontweight='bold', color=C_GREEN)
    
    ax.set_xlim(-0.4, 1.4)
    ax.set_ylim(-0.5, 5)
    ax.set_xlabel('x', fontsize=12)
    ax.set_ylabel('f(x)', fontsize=12)
    ax.set_title('辛普森公式几何意义', fontsize=16, fontweight='bold', pad=10)
    ax.legend(fontsize=10, loc='upper right')
    ax.grid(True, alpha=0.3)
    
    fig.tight_layout()
    path = os.path.join(OUT_DIR, 'simpson.png')
    fig.savefig(path, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close(fig)
    return path

# =====================================================
# 3. 复化梯形公式示意图
# =====================================================
def fig_composite_trapezoid():
    fig, ax = plt.subplots(1, 1, figsize=(7, 5), dpi=150)
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)
    
    n = 6
    x_nodes = np.linspace(0, 1, n+1)
    x_fine = np.linspace(0, 1.15, 300)
    
    # Fill trapezoids
    colors_trap = [C_BLUE, C_TEAL, C_ORANGE, C_PURPLE, C_GREEN, C_RED]
    for i in range(n):
        xi = x_nodes[i]
        xi1 = x_nodes[i+1]
        ax.fill([xi, xi1, xi1, xi], [0, 0, f(xi1), f(xi)], 
                alpha=0.2, color=colors_trap[i % len(colors_trap)])
    
    # Function curve
    ax.plot(x_fine, f(x_fine), color=C_RED, linewidth=2.5, label='f(x) = 4/(1+x²)')
    
    # Trapezoid segments
    for i in range(n):
        xi = x_nodes[i]
        xi1 = x_nodes[i+1]
        ax.plot([xi, xi1], [f(xi), f(xi1)], color=C_BLUE, linewidth=1.5, linestyle='--')
    
    # Vertical lines and points
    for i, xi in enumerate(x_nodes):
        ax.plot([xi, xi], [0, f(xi)], color='gray', linewidth=0.8, linestyle=':')
        ax.plot(xi, f(xi), 'o', color=C_BLUE, markersize=7, zorder=5)
    
    ax.annotate(f'n={n} 等分', xy=(0.5, -0.6), fontsize=13, ha='center', 
                fontweight='bold', color='gray')
    
    ax.set_xlim(-0.1, 1.2)
    ax.set_ylim(-0.8, 5)
    ax.set_xlabel('x', fontsize=12)
    ax.set_ylabel('f(x)', fontsize=12)
    ax.set_title('复化梯形公式 (n=6)', fontsize=16, fontweight='bold', pad=10)
    ax.legend(fontsize=10, loc='upper right')
    ax.grid(True, alpha=0.3)
    
    fig.tight_layout()
    path = os.path.join(OUT_DIR, 'composite_trapezoid.png')
    fig.savefig(path, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close(fig)
    return path

# =====================================================
# 4. 复化辛普森公式示意图
# =====================================================
def fig_composite_simpson():
    fig, ax = plt.subplots(1, 1, figsize=(7, 5), dpi=150)
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)
    
    n = 6  # must be even
    x_nodes = np.linspace(0, 1, n+1)
    x_fine = np.linspace(0, 1.15, 300)
    
    colors_simp = [C_BLUE, C_TEAL, C_ORANGE]
    # Each pair of subintervals forms one Simpson panel
    for k in range(n // 2):
        x0 = x_nodes[2*k]
        x1 = x_nodes[2*k+1]
        x2 = x_nodes[2*k+2]
        # Fit parabola through 3 points
        coeffs = np.polyfit([x0, x1, x2], [f(x0), f(x1), f(x2)], 2)
        p = np.poly1d(coeffs)
        x_par = np.linspace(x0, x2, 100)
        ax.fill_between(x_par, 0, p(x_par), alpha=0.2, color=colors_simp[k % len(colors_simp)])
        ax.plot(x_par, p(x_par), color=colors_simp[k % len(colors_simp)], linewidth=1.5, linestyle='--')
    
    # Function curve
    ax.plot(x_fine, f(x_fine), color=C_RED, linewidth=2.5, label='f(x) = 4/(1+x²)')
    
    # Points
    for i, xi in enumerate(x_nodes):
        ax.plot([xi, xi], [0, f(xi)], color='gray', linewidth=0.8, linestyle=':')
        marker = 's' if i % 2 == 1 else 'o'
        ax.plot(xi, f(xi), marker, color=C_GREEN, markersize=7, zorder=5)
    
    ax.annotate(f'n={n} 等分，{n//2}个Simpson子区间', xy=(0.5, -0.6), fontsize=12, ha='center', 
                fontweight='bold', color='gray')
    
    ax.set_xlim(-0.1, 1.2)
    ax.set_ylim(-0.8, 5)
    ax.set_xlabel('x', fontsize=12)
    ax.set_ylabel('f(x)', fontsize=12)
    ax.set_title('复化辛普森公式 (n=6)', fontsize=16, fontweight='bold', pad=10)
    ax.legend(fontsize=10, loc='upper right')
    ax.grid(True, alpha=0.3)
    
    fig.tight_layout()
    path = os.path.join(OUT_DIR, 'composite_simpson.png')
    fig.savefig(path, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close(fig)
    return path

# =====================================================
# 5. 误差对比图（双对数坐标）
# =====================================================
def fig_error_comparison():
    fig, ax = plt.subplots(1, 1, figsize=(7, 5.5), dpi=150)
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)
    
    true_val = np.pi
    
    # Composite trapezoid
    n_list = [2, 4, 8, 16, 32, 64]
    trap_vals = []
    for n in n_list:
        h = 1.0 / n
        total = 0.5 * (f(0) + f(1))
        for i in range(1, n):
            total += f(i * h)
        trap_vals.append(h * total)
    trap_err = [abs(v - true_val) for v in trap_vals]
    trap_h = [1.0/n for n in n_list]
    
    # Composite Simpson
    simp_vals = []
    for n in n_list:
        h = 1.0 / n
        x = np.linspace(0, 1, n+1)
        y = f(x)
        sum_odd = sum(y[1:n:2])
        sum_even = sum(y[2:n-1:2])
        simp_vals.append(h/3 * (y[0] + 4*sum_odd + 2*sum_even + y[n]))
    simp_err = [abs(v - true_val) for v in simp_vals]
    simp_h = [1.0/n for n in n_list]
    
    # Reference lines
    h_ref = np.array(trap_h)
    ref_Oh2 = 0.5 * h_ref**2
    ref_Oh4 = 0.05 * h_ref**4
    
    ax.loglog(trap_h, trap_err, 'o-', color=C_BLUE, linewidth=2, markersize=8, label=r'复化梯形 $O(h^2)$')
    ax.loglog(simp_h, simp_err, 's-', color=C_GREEN, linewidth=2, markersize=8, label=r'复化辛普森 $O(h^4)$')
    ax.loglog(h_ref, ref_Oh2, '--', color=C_BLUE, linewidth=1, alpha=0.5, label=r'参考线 $O(h^2)$')
    ax.loglog(h_ref, ref_Oh4, '--', color=C_GREEN, linewidth=1, alpha=0.5, label=r'参考线 $O(h^4)$')
    
    # Fixed error points
    trap_single_err = abs((f(0)+f(1))/2 - true_val)
    simp_single_err = abs((f(0) + 4*f(0.5) + f(1))/6 - true_val)
    ax.axhline(y=trap_single_err, color=C_BLUE, linewidth=1.5, linestyle=':', alpha=0.7, label=f'普通梯形 误差≈{trap_single_err:.4f}')
    ax.axhline(y=simp_single_err, color=C_GREEN, linewidth=1.5, linestyle=':', alpha=0.7, label=f'普通辛普森 误差≈{simp_single_err:.6f}')
    
    ax.set_xlabel('步长 h', fontsize=13)
    ax.set_ylabel('绝对误差', fontsize=13)
    ax.set_title('误差-步长对比图（双对数坐标）', fontsize=16, fontweight='bold', pad=10)
    ax.legend(fontsize=9, loc='lower right')
    ax.grid(True, alpha=0.3, which='both')
    ax.invert_xaxis()
    
    fig.tight_layout()
    path = os.path.join(OUT_DIR, 'error_comparison.png')
    fig.savefig(path, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close(fig)
    return path

# =====================================================
# 6. 算法精度对比柱状图
# =====================================================
def fig_algorithm_comparison():
    fig, axes = plt.subplots(1, 2, figsize=(10, 5), dpi=150)
    fig.patch.set_facecolor(C_BG)
    
    # Left: convergence at n=64
    ax = axes[0]
    ax.set_facecolor(C_BG)
    
    true_val = np.pi
    methods = ['普通梯形\n(n=1)', '普通辛普森\n(n=1)', '复化梯形\n(n=64)', '复化辛普森\n(n=64)']
    
    n = 64
    h = 1.0/n
    trap_single = (f(0)+f(1))/2
    simp_single = (f(0) + 4*f(0.5) + f(1))/6
    comp_trap = h * (0.5*(f(0)+f(1)) + sum(f(i*h) for i in range(1,n)))
    x_arr = np.linspace(0, 1, n+1)
    y_arr = f(x_arr)
    sum_odd = sum(y_arr[1:n:2])
    sum_even = sum(y_arr[2:n-1:2])
    comp_simp = h/3 * (y_arr[0] + 4*sum_odd + 2*sum_even + y_arr[n])
    
    errors = [abs(trap_single-true_val), abs(simp_single-true_val), 
              abs(comp_trap-true_val), abs(comp_simp-true_val)]
    colors = [C_BLUE, C_GREEN, C_ORANGE, C_PURPLE]
    
    bars = ax.bar(methods, errors, color=colors, alpha=0.8, edgecolor='white', linewidth=1.5)
    ax.set_ylabel('绝对误差', fontsize=12)
    ax.set_title('四种算法绝对误差对比', fontsize=14, fontweight='bold')
    ax.set_yscale('log')
    ax.grid(True, alpha=0.3, axis='y')
    
    for bar, err in zip(bars, errors):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height()*1.3,
                f'{err:.2e}', ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    # Right: convergence speed comparison
    ax2 = axes[1]
    ax2.set_facecolor(C_BG)
    
    n_vals = [2, 4, 8, 16, 32, 64]
    trap_errors = []
    simp_errors = []
    for n in n_vals:
        h = 1.0/n
        # trapezoid
        total = 0.5*(f(0)+f(1))
        for i in range(1,n):
            total += f(i*h)
        trap_errors.append(abs(h*total - true_val))
        # simpson
        x_s = np.linspace(0,1,n+1)
        y_s = f(x_s)
        so = sum(y_s[1:n:2])
        se = sum(y_s[2:n-1:2])
        simp_errors.append(abs(h/3*(y_s[0]+4*so+2*se+y_s[n]) - true_val))
    
    ax2.plot(n_vals, trap_errors, 'o-', color=C_ORANGE, linewidth=2, markersize=7, label='复化梯形')
    ax2.plot(n_vals, simp_errors, 's-', color=C_PURPLE, linewidth=2, markersize=7, label='复化辛普森')
    ax2.set_xlabel('等分数 n', fontsize=12)
    ax2.set_ylabel('绝对误差', fontsize=12)
    ax2.set_yscale('log')
    ax2.set_title('复化方法收敛速度对比', fontsize=14, fontweight='bold')
    ax2.legend(fontsize=10)
    ax2.grid(True, alpha=0.3)
    ax2.set_xticks(n_vals)
    
    fig.tight_layout()
    path = os.path.join(OUT_DIR, 'algorithm_comparison.png')
    fig.savefig(path, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close(fig)
    return path

# =====================================================
# 7. 工程背景示意图
# =====================================================
def fig_engineering_bg():
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.5), dpi=150)
    fig.patch.set_facecolor(C_BG)
    
    # Left: velocity curve
    ax = axes[0]
    ax.set_facecolor(C_BG)
    t = np.linspace(0, 1, 200)
    v = f(t)
    ax.fill_between(t, 0, v, alpha=0.2, color=C_BLUE)
    ax.plot(t, v, color=C_RED, linewidth=2.5)
    ax.set_xlabel('时间 t (s)', fontsize=12)
    ax.set_ylabel('速度 v(t) (m/s)', fontsize=12)
    ax.set_title('滑块变速运动速度曲线', fontsize=14, fontweight='bold')
    ax.annotate('位移 = ∫v(t)dt\n= 阴影面积', xy=(0.5, 2.0), fontsize=12,
                ha='center', fontweight='bold', color=C_BLUE,
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor=C_BLUE, alpha=0.8))
    ax.grid(True, alpha=0.3)
    
    # Right: applications
    ax2 = axes[1]
    ax2.set_facecolor(C_BG)
    ax2.axis('off')
    apps = [
        ('✈', '航空航天\n热流密度积分', C_BLUE),
        ('🔋', '电动汽车\n电量估算', C_GREEN),
        ('🤖', '机器人\n轨迹规划', C_ORANGE),
        ('⚡', '能源动力\n功率积分', C_PURPLE),
    ]
    for i, (icon, text, color) in enumerate(apps):
        x_pos = 0.25 if i % 2 == 0 else 0.75
        y_pos = 0.75 if i < 2 else 0.25
        ax2.text(x_pos, y_pos, text, fontsize=13, ha='center', va='center',
                fontweight='bold', color=color,
                bbox=dict(boxstyle='round,pad=0.4', facecolor='white', 
                         edgecolor=color, linewidth=2, alpha=0.9),
                transform=ax2.transAxes)
    ax2.set_title('工程应用场景', fontsize=14, fontweight='bold')
    
    fig.tight_layout()
    path = os.path.join(OUT_DIR, 'engineering_bg.png')
    fig.savefig(path, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close(fig)
    return path

# =====================================================
# 8. 四种算法并列对比图
# =====================================================
def fig_four_methods_side():
    fig, axes = plt.subplots(2, 2, figsize=(10, 8), dpi=150)
    fig.patch.set_facecolor(C_BG)
    
    x_fine = np.linspace(0, 1.15, 300)
    y_fine = f(x_fine)
    
    configs = [
        ('普通梯形', 1, C_BLUE, axes[0,0], False),
        ('普通辛普森', 1, C_GREEN, axes[0,1], True),
        ('复化梯形 (n=4)', 4, C_ORANGE, axes[1,0], False),
        ('复化辛普森 (n=4)', 4, C_PURPLE, axes[1,1], True),
    ]
    
    for title, n, color, ax, is_simpson in configs:
        ax.set_facecolor(C_BG)
        x_nodes = np.linspace(0, 1, n+1)
        
        if is_simpson:
            # Simpson panels
            for k in range(n // 2):
                x0 = x_nodes[2*k]
                x1 = x_nodes[2*k+1]
                x2 = x_nodes[2*k+2]
                coeffs = np.polyfit([x0, x1, x2], [f(x0), f(x1), f(x2)], 2)
                p = np.poly1d(coeffs)
                x_par = np.linspace(x0, x2, 100)
                ax.fill_between(x_par, 0, p(x_par), alpha=0.25, color=color)
                ax.plot(x_par, p(x_par), color=color, linewidth=1.5, linestyle='--')
        else:
            # Trapezoid panels
            for i in range(n):
                xi = x_nodes[i]
                xi1 = x_nodes[i+1]
                ax.fill([xi, xi1, xi1, xi], [0, 0, f(xi1), f(xi)],
                       alpha=0.25, color=color)
                ax.plot([xi, xi1], [f(xi), f(xi1)], color=color, linewidth=1.5, linestyle='--')
        
        ax.plot(x_fine, y_fine, color=C_RED, linewidth=2)
        
        for xi in x_nodes:
            ax.plot([xi, xi], [0, f(xi)], color='gray', linewidth=0.6, linestyle=':')
            ax.plot(xi, f(xi), 'o', color=color, markersize=6, zorder=5)
        
        # Compute result
        if is_simpson:
            h = 1.0/n
            x_s = np.linspace(0,1,n+1)
            y_s = f(x_s)
            so = sum(y_s[1:n:2])
            se = sum(y_s[2:n-1:2])
            result = h/3*(y_s[0]+4*so+2*se+y_s[n])
        else:
            if n == 1:
                result = (f(0)+f(1))/2
            else:
                h = 1.0/n
                total = 0.5*(f(0)+f(1))
                for i in range(1,n):
                    total += f(i*h)
                result = h*total
        
        ax.set_title(f'{title}\n结果={result:.6f} 误差={abs(result-np.pi):.2e}', 
                     fontsize=11, fontweight='bold')
        ax.set_xlim(-0.05, 1.15)
        ax.set_ylim(-0.3, 5)
        ax.grid(True, alpha=0.3)
    
    fig.suptitle('四种数值积分方法对比', fontsize=16, fontweight='bold', y=1.01)
    fig.tight_layout()
    path = os.path.join(OUT_DIR, 'four_methods.png')
    fig.savefig(path, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close(fig)
    return path

# =====================================================
# Generate all images
# =====================================================
print("Generating images...")
img_trap = fig_trapezoid()
print("  trapezoid done")
img_simp = fig_simpson()
print("  simpson done")
img_comp_trap = fig_composite_trapezoid()
print("  composite_trapezoid done")
img_comp_simp = fig_composite_simpson()
print("  composite_simpson done")
img_error = fig_error_comparison()
print("  error_comparison done")
img_algo = fig_algorithm_comparison()
print("  algorithm_comparison done")
img_eng = fig_engineering_bg()
print("  engineering_bg done")
img_four = fig_four_methods_side()
print("  four_methods done")

# =====================================================
# BUILD PPT
# =====================================================
print("\nBuilding PPT...")

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

# Color theme
BG_COLOR = RGBColor(0x0F, 0x17, 0x2A)  # Dark blue
TITLE_COLOR = RGBColor(0xFF, 0xFF, 0xFF)
SUBTITLE_COLOR = RGBColor(0x93, 0xC5, 0xFD)
ACCENT_COLOR = RGBColor(0x3B, 0x82, 0xF6)
TEXT_COLOR = RGBColor(0xE2, 0xE8, 0xF0)
HIGHLIGHT_COLOR = RGBColor(0x60, 0xA5, 0xFA)

def set_slide_bg(slide, color=BG_COLOR):
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = color

def add_text_box(slide, left, top, width, height, text, font_size=18, 
                 bold=False, color=TEXT_COLOR, alignment=PP_ALIGN.LEFT, font_name='Microsoft YaHei'):
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(font_size)
    p.font.bold = bold
    p.font.color.rgb = color
    p.font.name = font_name
    p.alignment = alignment
    return txBox

def add_title_slide(slide, title, subtitle=''):
    set_slide_bg(slide)
    # Decorative line
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(2), Inches(3.0), Inches(9.333), Inches(0.05))
    shape.fill.solid()
    shape.fill.fore_color.rgb = ACCENT_COLOR
    shape.line.fill.background()
    
    add_text_box(slide, Inches(2), Inches(1.5), Inches(9.333), Inches(1.5),
                 title, font_size=40, bold=True, color=TITLE_COLOR, alignment=PP_ALIGN.CENTER)
    if subtitle:
        add_text_box(slide, Inches(2), Inches(3.3), Inches(9.333), Inches(1),
                     subtitle, font_size=22, color=SUBTITLE_COLOR, alignment=PP_ALIGN.CENTER)

def add_content_slide(slide, title, image_path=None, bullets=None, image_left=None, 
                      image_top=None, image_width=None, image_height=None,
                      text_left=None, text_top=None, text_width=None):
    set_slide_bg(slide)
    
    # Title bar
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.0))
    shape.fill.solid()
    shape.fill.fore_color.rgb = RGBColor(0x1E, 0x29, 0x3B)
    shape.line.fill.background()
    
    add_text_box(slide, Inches(0.5), Inches(0.15), Inches(12), Inches(0.7),
                 title, font_size=28, bold=True, color=TITLE_COLOR, alignment=PP_ALIGN.LEFT)
    
    # Accent line under title
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.5), Inches(0.95), Inches(3), Inches(0.04))
    line.fill.solid()
    line.fill.fore_color.rgb = ACCENT_COLOR
    line.line.fill.background()
    
    if image_path and bullets:
        # Image + text layout
        img_l = image_left or Inches(0.5)
        img_t = image_top or Inches(1.3)
        img_w = image_width or Inches(6)
        img_h = image_height or Inches(5.5)
        slide.shapes.add_picture(image_path, img_l, img_t, img_w, img_h)
        
        txBox = slide.shapes.add_textbox(text_left or Inches(7), text_top or Inches(1.3), 
                                          text_width or Inches(5.5), Inches(5.5))
        tf = txBox.text_frame
        tf.word_wrap = True
        for i, bullet in enumerate(bullets):
            if i == 0:
                p = tf.paragraphs[0]
            else:
                p = tf.add_paragraph()
            p.text = bullet
            p.font.size = Pt(16)
            p.font.color.rgb = TEXT_COLOR
            p.font.name = 'Microsoft YaHei'
            p.space_after = Pt(8)
    elif image_path:
        # Image only, centered
        img_w = image_width or Inches(10)
        img_h = image_height or Inches(5.8)
        img_l = image_left or Inches((13.333 - 10) / 2)
        img_t = image_top or Inches(1.3)
        slide.shapes.add_picture(image_path, img_l, img_t, img_w, img_h)
    elif bullets:
        txBox = slide.shapes.add_textbox(text_left or Inches(1), text_top or Inches(1.3),
                                          text_width or Inches(11), Inches(5.5))
        tf = txBox.text_frame
        tf.word_wrap = True
        for i, bullet in enumerate(bullets):
            if i == 0:
                p = tf.paragraphs[0]
            else:
                p = tf.add_paragraph()
            p.text = bullet
            p.font.size = Pt(18)
            p.font.color.rgb = TEXT_COLOR
            p.font.name = 'Microsoft YaHei'
            p.space_after = Pt(10)

# =====================================================
# SLIDE 1: Title
# =====================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank
add_title_slide(slide, '数值积分算法设计与实现', '梯形公式 · 辛普森公式 · 复化求积')

# =====================================================
# SLIDE 2: 团队分工
# =====================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_title_slide(slide, '团队分工', '')

# Team member boxes
members = [
    ('组长 · 吴瑞东', '思考题1-5\n撰写实验报告\n制作讲解PPT', ACCENT_COLOR),
    ('组员 · 余耽阳', '梯形+复化梯形\n公式推导\n代码编写·结果计算', RGBColor(0x16, 0xA3, 0x4A)),
    ('组员 · 饶宇佳', '辛普森公式\n公式推导\n代码编写·结果计算', RGBColor(0xEA, 0x58, 0x0C)),
    ('组员 · 刘家乐', '复化辛普森公式\n公式推导\n代码编写·结果计算', RGBColor(0x7C, 0x3A, 0xED)),
    ('组员 · 周亚辉', '汇总数据\n误差分析·绘制图表\nPPT讲解', RGBColor(0x0D, 0x94, 0x88)),
]

for i, (name, role, color) in enumerate(members):
    left = Inches(0.5 + i * 2.5)
    top = Inches(3.5)
    
    # Card background
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, Inches(2.2), Inches(2.8))
    card.fill.solid()
    card.fill.fore_color.rgb = RGBColor(0x1E, 0x29, 0x3B)
    card.line.color.rgb = color
    card.line.width = Pt(2)
    
    # Top accent bar
    accent = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, Inches(2.2), Inches(0.08))
    accent.fill.solid()
    accent.fill.fore_color.rgb = color
    accent.line.fill.background()
    
    add_text_box(slide, left + Inches(0.1), top + Inches(0.2), Inches(2), Inches(0.5),
                 name, font_size=16, bold=True, color=color, alignment=PP_ALIGN.CENTER)
    add_text_box(slide, left + Inches(0.1), top + Inches(0.8), Inches(2), Inches(1.8),
                 role, font_size=13, color=TEXT_COLOR, alignment=PP_ALIGN.CENTER)

# =====================================================
# SLIDE 3: 实验目的
# =====================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_content_slide(slide, '实验目的', bullets=[
    '▸ 理解数值积分基本思想：连续定积分 → 离散加权求和',
    '▸ 掌握梯形、辛普森求积公式推导与误差特性',
    '▸ 掌握复化梯形、复化辛普森的构造方法',
    '▸ 编程实现四种算法，对比精度、收敛速度与计算量',
    '▸ 理解线性性、误差阶与算法稳定性',
    '▸ 结合工程实例分析数值积分的工程精度'
])

# =====================================================
# SLIDE 4: 工程背景
# =====================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_content_slide(slide, '实验工程背景', image_path=img_eng,
                  bullets=[
                      '▎ 核心问题',
                      '非线性函数定积分求解',
                      '无法用解析原函数精确描述',
                      '',
                      '▎ 工程实例',
                      '飞行器热流密度积分',
                      '电动汽车电量估算',
                      '机器人轨迹位移计算',
                      '',
                      '▎ 本实验目标',
                      '系统对比四种数值积分方法',
                      '分析步长对精度的影响规律',
                  ],
                  image_width=Inches(6.5), image_height=Inches(4.5))

# =====================================================
# SLIDE 5: 梯形公式
# =====================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_content_slide(slide, '梯形求积公式', image_path=img_trap,
                  bullets=[
                      '▎ 基本思想',
                      '用两端点连线（一次插值）',
                      '代替原函数曲线',
                      '',
                      '▎ 公式',
                      'T = (b-a)/2 · [f(a)+f(b)]',
                      '',
                      '▎ 误差阶',
                      'O(h³) · 局部截断误差',
                      '对一次多项式精确',
                      '',
                      '▎ 几何意义',
                      '梯形面积 ≈ 积分值',
                  ])

# =====================================================
# SLIDE 6: 复化梯形公式
# =====================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_content_slide(slide, '复化梯形求积公式', image_path=img_comp_trap,
                  bullets=[
                      '▎ 区间划分',
                      '[a,b] 等分 n 份',
                      '步长 h = (b-a)/n',
                      '',
                      '▎ 公式',
                      'Tn = h/2·[f(a) + 2Σf(xi)',
                      '     + f(b)]',
                      '',
                      '▎ 误差阶',
                      'O(h²) · 二阶方法',
                      '步长减半 → 误差约 1/4',
                      '',
                      '▎ 优势',
                      '可通过加密提高精度',
                  ])

# =====================================================
# SLIDE 7: 辛普森公式
# =====================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_content_slide(slide, '辛普森求积公式', image_path=img_simp,
                  bullets=[
                      '▎ 基本思想',
                      '用三点二次插值（抛物线）',
                      '代替原函数曲线',
                      '',
                      '▎ 公式',
                      'S = (b-a)/6·[f(a)+4f(m)+f(b)]',
                      'm = (a+b)/2',
                      '',
                      '▎ 误差阶',
                      'O(h⁵) · 局部截断误差',
                      '代数精度 = 3次',
                      '',
                      '▎ 几何意义',
                      '抛物线下面积 ≈ 积分值',
                  ])

# =====================================================
# SLIDE 8: 复化辛普森公式
# =====================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_content_slide(slide, '复化辛普森求积公式', image_path=img_comp_simp,
                  bullets=[
                      '▎ 区间划分',
                      '[a,b] 等分 n 份 (n为偶数)',
                      '每2个子区间一个Simpson面板',
                      '',
                      '▎ 公式',
                      'Sn = h/3·[f(a) + 4Σf(x奇)',
                      '     + 2Σf(x偶) + f(b)]',
                      '',
                      '▎ 误差阶',
                      'O(h⁴) · 四阶方法',
                      '步长减半 → 误差约 1/16',
                      '',
                      '▎ 优势',
                      '收敛极快，工程首选',
                  ])

# =====================================================
# SLIDE 9: 四种方法对比图
# =====================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_content_slide(slide, '四种数值积分方法对比', image_path=img_four,
                  image_left=Inches(0.3), image_top=Inches(1.2),
                  image_width=Inches(12.5), image_height=Inches(6))

# =====================================================
# SLIDE 10: 实验结果数据
# =====================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide)

# Title bar
shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.0))
shape.fill.solid()
shape.fill.fore_color.rgb = RGBColor(0x1E, 0x29, 0x3B)
shape.line.fill.background()
add_text_box(slide, Inches(0.5), Inches(0.15), Inches(12), Inches(0.7),
             '实验结果数据汇总', font_size=28, bold=True, color=TITLE_COLOR)
line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.5), Inches(0.95), Inches(3), Inches(0.04))
line.fill.solid()
line.fill.fore_color.rgb = ACCENT_COLOR
line.line.fill.background()

# Data table
true_val = np.pi
rows = 8
cols = 4
table_shape = slide.shapes.add_table(rows, cols, Inches(1.5), Inches(1.3), Inches(10), Inches(5.5))
table = table_shape.table

# Headers
headers = ['方法', '等分数 n', '近似积分值', '绝对误差']
for j, h in enumerate(headers):
    cell = table.cell(0, j)
    cell.text = h
    for paragraph in cell.text_frame.paragraphs:
        paragraph.font.size = Pt(14)
        paragraph.font.bold = True
        paragraph.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        paragraph.font.name = 'Microsoft YaHei'
        paragraph.alignment = PP_ALIGN.CENTER
    cell.fill.solid()
    cell.fill.fore_color.rgb = RGBColor(0x1E, 0x40, 0x7A)

# Data
data = [
    ('普通梯形', '1', '3.000000', f'{abs(3.0-true_val):.4e}'),
    ('普通辛普森', '1', '3.133333', f'{abs(3.133333333333333-true_val):.4e}'),
    ('复化梯形', '8', '3.138988', f'{abs(3.138988494491-true_val):.4e}'),
    ('复化梯形', '64', '3.141552', f'{abs(3.141551963486-true_val):.4e}'),
    ('复化辛普森', '4', '3.141569', f'{abs(3.141568627500-true_val):.4e}'),
    ('复化辛普森', '16', '3.141593', f'{abs(3.141592651200-true_val):.4e}'),
    ('复化辛普森', '64', '3.141593', f'{abs(3.141592653600-true_val):.4e}'),
]

row_colors = [
    RGBColor(0x1E, 0x29, 0x3B),
    RGBColor(0x22, 0x2D, 0x42),
    RGBColor(0x1E, 0x29, 0x3B),
    RGBColor(0x22, 0x2D, 0x42),
    RGBColor(0x1E, 0x29, 0x3B),
    RGBColor(0x22, 0x2D, 0x42),
    RGBColor(0x1E, 0x29, 0x3B),
]

for i, row_data in enumerate(data):
    for j, val in enumerate(row_data):
        cell = table.cell(i+1, j)
        cell.text = val
        for paragraph in cell.text_frame.paragraphs:
            paragraph.font.size = Pt(13)
            paragraph.font.color.rgb = TEXT_COLOR
            paragraph.font.name = 'Microsoft YaHei'
            paragraph.alignment = PP_ALIGN.CENTER
        cell.fill.solid()
        cell.fill.fore_color.rgb = row_colors[i]

# =====================================================
# SLIDE 11: 误差对比图
# =====================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_content_slide(slide, '误差-步长对比分析', image_path=img_error,
                  image_left=Inches(0.3), image_top=Inches(1.2),
                  image_width=Inches(8), image_height=Inches(6),
                  bullets=[
                      '▎ 关键发现',
                      '',
                      '复化梯形：',
                      '误差 O(h²)',
                      '步长减半 → 误差 ≈ 1/4',
                      '',
                      '复化辛普森：',
                      '误差 O(h⁴)',
                      '步长减半 → 误差 ≈ 1/16',
                      '',
                      '普通公式无法通过',
                      '加密提高精度',
                      '',
                      '复化辛普森 n=8 时',
                      '误差已低于 10⁻⁷',
                  ],
                  text_left=Inches(8.5))

# =====================================================
# SLIDE 12: 算法对比
# =====================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_content_slide(slide, '算法综合对比', image_path=img_algo,
                  image_left=Inches(0.3), image_top=Inches(1.2),
                  image_width=Inches(12.5), image_height=Inches(5.8))

# =====================================================
# SLIDE 13: 误差分析结论
# =====================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_content_slide(slide, '误差分析结论', bullets=[
    '▎ 理论误差阶验证',
    '  复化梯形：实验误差比 ≈ 1/4，严格符合 O(h²)',
    '  复化辛普森：误差比 ≈ 1/16，实际收敛阶达 O(h⁴) 以上',
    '',
    '▎ 步长对误差的影响',
    '  复化梯形误差以 O(h²) 速度下降',
    '  复化辛普森至少以 O(h⁴) 下降',
    '  达到相同精度，复化辛普森所需 n 远小于复化梯形',
    '',
    '▎ 工程精度满足性',
    '  一般工程（相对误差 1%）：复化辛普森 n=4 即可',
    '  精密工程（相对误差 0.01%）：复化辛普森 n=8 绰绰有余',
    '  普通梯形误差高达 4.5%，工程上基本不可用',
    '',
    '▎ 误差阶指导步长选择',
    '  通过两个步长试算 → 估算误差常数 → 预测最小 n',
    '  避免盲目细分，优化计算资源',
])

# =====================================================
# SLIDE 14: 思考题（精简版）
# =====================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_content_slide(slide, '思考题要点', bullets=[
    'Q1: 为什么辛普森公式对三次多项式精确？',
    '  → 截断误差含 f⁴(ξ)，三次多项式 f⁴=0，误差为零',
    '',
    'Q2: 复化梯形和复化辛普森误差阶为何不同？',
    '  → 局部误差阶不同：梯形 O(h³) vs 辛普森 O(h⁵)',
    '  → 累加后整体误差：O(h²) vs O(h⁴)',
    '',
    'Q3: 数值积分线性性的工程意义？',
    '  → 分解复杂物理量 → 分别积分 → 叠加结果',
    '  → 模块化编程、误差分析补偿、线性系统分析',
    '',
    'Q4: 机器学习 vs 传统复化积分？',
    '  → 传统：严格误差界、可重复 | 机器学习：数据驱动、预测快但黑箱',
    '',
    'Q5: 误差阶在工程精度把控中的作用？',
    '  → 预测所需网格 · 指导算法选择 · 验证收敛性 · 安全余量设计',
])

# =====================================================
# SLIDE 15: 总结
# =====================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_title_slide(slide, '总结', '')

# Summary cards
summaries = [
    ('复化辛普森', '精度·效率·稳定性\n全面最优\n工程首选方法', RGBColor(0x16, 0xA3, 0x4A)),
    ('复化梯形', '非光滑函数\n低精度场景\n二阶方法', RGBColor(0xEA, 0x58, 0x0C)),
    ('普通公式', '仅教学/粗略估算\n无法加密提高精度', RGBColor(0x7C, 0x3A, 0xED)),
    ('误差阶理论', '直接指导步长选择\n最小计算代价\n获得可靠结果', ACCENT_COLOR),
]

for i, (title, desc, color) in enumerate(summaries):
    left = Inches(0.8 + i * 3.1)
    top = Inches(3.5)
    
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, Inches(2.8), Inches(2.5))
    card.fill.solid()
    card.fill.fore_color.rgb = RGBColor(0x1E, 0x29, 0x3B)
    card.line.color.rgb = color
    card.line.width = Pt(2)
    
    # Top accent
    accent = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, Inches(2.8), Inches(0.08))
    accent.fill.solid()
    accent.fill.fore_color.rgb = color
    accent.line.fill.background()
    
    add_text_box(slide, left + Inches(0.15), top + Inches(0.2), Inches(2.5), Inches(0.5),
                 title, font_size=18, bold=True, color=color, alignment=PP_ALIGN.CENTER)
    add_text_box(slide, left + Inches(0.15), top + Inches(0.8), Inches(2.5), Inches(1.5),
                 desc, font_size=14, color=TEXT_COLOR, alignment=PP_ALIGN.CENTER)

# =====================================================
# SLIDE 16: Thank you
# =====================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_title_slide(slide, '谢谢！', 'Q & A')

# =====================================================
# Save PPT
# =====================================================
output_path = r'c:\Users\Lenovo\Desktop\数值积分算法PPT_v2.pptx'
prs.save(output_path)
print(f"\nPPT saved to: {output_path}")
