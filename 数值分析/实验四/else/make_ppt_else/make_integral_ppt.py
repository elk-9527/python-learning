# -*- coding: utf-8 -*-
"""
数值积分算法设计与实现 PPT 自动生成脚本
主题：梯形公式、辛普森公式、复化求积
特点：多图、多表、少文字

运行前安装：
pip install python-pptx matplotlib numpy
"""

import math
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR


# =========================
# 1. 基础配置
# =========================

OUT_FILE = "数值积分算法设计与实现_汇报PPT.pptx"
ASSET_DIR = Path("ppt_assets")
ASSET_DIR.mkdir(exist_ok=True)

plt.rcParams["font.sans-serif"] = [
    "Microsoft YaHei",
    "SimHei",
    "Arial Unicode MS",
    "DejaVu Sans"
]
plt.rcParams["axes.unicode_minus"] = False

FONT = "Microsoft YaHei"

C = {
    "navy": "#0B132B",
    "blue": "#1C5D99",
    "cyan": "#3FA7D6",
    "teal": "#00A896",
    "orange": "#F28C28",
    "red": "#E63946",
    "purple": "#6A4C93",
    "green": "#2A9D8F",
    "gray": "#6C757D",
    "light": "#F7F9FC",
    "white": "#FFFFFF",
    "black": "#111111",
    "table_alt": "#EEF4FA",
    "yellow": "#FFD166"
}


def rgb(hex_color):
    hex_color = hex_color.replace("#", "")
    return RGBColor(
        int(hex_color[0:2], 16),
        int(hex_color[2:4], 16),
        int(hex_color[4:6], 16)
    )


def fmt_num(x, digits=12):
    return f"{x:.{digits}f}"


def fmt_err(x):
    return f"{x:.3e}"


# =========================
# 2. 数值积分数据
# =========================

a, b = 0.0, 1.0
true_value = math.pi


def vf(x):
    return 4.0 / (1.0 + x * x)


def v(x):
    x = np.asarray(x)
    return 4.0 / (1.0 + x * x)


def trapezoid_single():
    return (b - a) * (vf(a) + vf(b)) / 2.0


def simpson_single():
    mid = (a + b) / 2.0
    return (b - a) / 6.0 * (vf(a) + 4 * vf(mid) + vf(b))


def composite_trapezoid(n):
    x = np.linspace(a, b, n + 1)
    y = v(x)
    h = (b - a) / n
    return h * (0.5 * y[0] + np.sum(y[1:-1]) + 0.5 * y[-1])


def composite_simpson(n):
    if n % 2 != 0:
        raise ValueError("复化辛普森公式要求 n 为偶数")
    x = np.linspace(a, b, n + 1)
    y = v(x)
    h = (b - a) / n
    return h / 3.0 * (
        y[0]
        + y[-1]
        + 4.0 * np.sum(y[1:-1:2])
        + 2.0 * np.sum(y[2:-1:2])
    )


def find_min_n_for_tol(method, tol=1e-6):
    if method == "trap":
        n = 1
        while abs(composite_trapezoid(n) - true_value) > tol:
            n += 1
        return n
    if method == "simp":
        n = 2
        while abs(composite_simpson(n) - true_value) > tol:
            n += 2
        return n
    raise ValueError(method)


n_list = np.array([2, 4, 8, 16, 32, 64])
h_list = 1.0 / n_list

T_single = trapezoid_single()
S_single = simpson_single()

Tn = np.array([composite_trapezoid(int(n)) for n in n_list])
Sn = np.array([composite_simpson(int(n)) for n in n_list])

err_T_single = abs(T_single - true_value)
err_S_single = abs(S_single - true_value)
err_Tn = np.abs(Tn - true_value)
err_Sn = np.abs(Sn - true_value)

tol = 1e-6
min_n_trap = find_min_n_for_tol("trap", tol)
min_n_simp = find_min_n_for_tol("simp", tol)

next_pow2_trap = 1 << (min_n_trap - 1).bit_length()


# =========================
# 3. 生成图表图片
# =========================

def savefig(path):
    plt.tight_layout()
    plt.savefig(path, dpi=220, bbox_inches="tight", facecolor="white")
    plt.close()


def make_curve_area_chart():
    t = np.linspace(0, 1, 500)
    y = v(t)

    fig, ax = plt.subplots(figsize=(7.2, 4.1))
    ax.plot(t, y, color=C["blue"], linewidth=3, label=r"$v(t)=\frac{4}{1+t^2}$")
    ax.fill_between(t, 0, y, color=C["cyan"], alpha=0.25)
    ax.scatter([0, 1], [vf(0), vf(1)], color=C["red"], zorder=5)

    ax.text(
        0.48,
        1.15,
        r"$S=\int_0^1 \frac{4}{1+t^2}dt=\pi$",
        fontsize=15,
        color=C["navy"],
        ha="center",
        bbox=dict(boxstyle="round,pad=0.35", fc="#FFFFFF", ec=C["blue"], lw=1.5)
    )

    ax.set_title("速度曲线与位移面积", fontsize=16, weight="bold")
    ax.set_xlabel("时间 t / s")
    ax.set_ylabel("速度 v(t)")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 4.4)
    ax.grid(alpha=0.25)
    ax.legend(loc="upper right")
    savefig(ASSET_DIR / "curve_area.png")


def make_trap_chart():
    t = np.linspace(0, 1, 500)
    y = v(t)

    fig, ax = plt.subplots(figsize=(7.2, 4.1))
    ax.plot(t, y, color=C["blue"], linewidth=3, label="真实曲线")
    ax.plot([0, 1], [vf(0), vf(1)], color=C["orange"], linewidth=3, label="端点连线")
    ax.fill([0, 1, 1, 0], [0, 0, vf(1), vf(0)], color=C["orange"], alpha=0.25)

    ax.scatter([0, 1], [vf(0), vf(1)], color=C["red"], s=60, zorder=5)
    ax.text(0.5, 3.25, "梯形面积近似", ha="center", fontsize=14, color=C["navy"])

    ax.set_title("普通梯形公式：用直线代替曲线", fontsize=16, weight="bold")
    ax.set_xlabel("t")
    ax.set_ylabel("v(t)")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 4.4)
    ax.grid(alpha=0.25)
    ax.legend()
    savefig(ASSET_DIR / "trap.png")


def make_simpson_chart():
    x3 = np.array([0.0, 0.5, 1.0])
    y3 = v(x3)
    coef = np.polyfit(x3, y3, 2)

    t = np.linspace(0, 1, 500)
    y_true = v(t)
    y_quad = np.polyval(coef, t)

    fig, ax = plt.subplots(figsize=(7.2, 4.1))
    ax.plot(t, y_true, color=C["blue"], linewidth=3, label="真实曲线")
    ax.plot(t, y_quad, color=C["purple"], linewidth=3, linestyle="--", label="二次插值抛物线")
    ax.fill_between(t, 0, y_quad, color=C["purple"], alpha=0.18)

    ax.scatter(x3, y3, color=C["red"], s=65, zorder=5)
    for xi, yi, lab in zip(x3, y3, ["a", "m", "b"]):
        ax.text(xi, yi + 0.18, lab, ha="center", fontsize=13, color=C["red"])

    ax.set_title("辛普森公式：用抛物线近似曲线", fontsize=16, weight="bold")
    ax.set_xlabel("t")
    ax.set_ylabel("v(t)")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 4.4)
    ax.grid(alpha=0.25)
    ax.legend()
    savefig(ASSET_DIR / "simpson.png")


def make_grid_chart():
    n = 8
    x = np.linspace(0, 1, n + 1)
    t = np.linspace(0, 1, 500)

    fig, ax = plt.subplots(figsize=(7.2, 4.1))
    ax.plot(t, v(t), color=C["blue"], linewidth=3)

    for i in range(n):
        color = C["cyan"] if i % 2 == 0 else C["teal"]
        ax.axvspan(x[i], x[i + 1], color=color, alpha=0.12)

    for xi in x:
        ax.axvline(xi, color=C["gray"], linewidth=0.8, alpha=0.7)

    ax.annotate(
        "",
        xy=(x[2], 0.45),
        xytext=(x[1], 0.45),
        arrowprops=dict(arrowstyle="<->", color=C["red"], lw=1.8)
    )
    ax.text((x[1] + x[2]) / 2, 0.62, "h", ha="center", color=C["red"], fontsize=14)

    ax.text(
        0.5,
        3.75,
        "复化求积：把大区间拆成小区间",
        ha="center",
        fontsize=14,
        color=C["navy"],
        bbox=dict(boxstyle="round,pad=0.35", fc="white", ec=C["blue"])
    )

    ax.set_title("区间等分与复化思想", fontsize=16, weight="bold")
    ax.set_xlabel("t")
    ax.set_ylabel("v(t)")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 4.4)
    ax.grid(alpha=0.2)
    savefig(ASSET_DIR / "grid.png")


def make_convergence_chart():
    fig, ax = plt.subplots(figsize=(7.4, 4.4))

    ax.loglog(h_list, err_Tn, "o-", color=C["orange"], linewidth=2.5, label="复化梯形")
    ax.loglog(h_list, err_Sn, "s-", color=C["purple"], linewidth=2.5, label="复化辛普森")

    ref_h = h_list
    ref2 = err_Tn[0] * (ref_h / ref_h[0]) ** 2
    ref4 = err_Sn[1] * (ref_h / ref_h[1]) ** 4

    ax.loglog(ref_h, ref2, "--", color=C["gray"], label=r"$O(h^2)$ 参考线")
    ax.loglog(ref_h, ref4, "--", color=C["green"], label=r"$O(h^4)$ 参考线")

    ax.axhline(tol, color=C["red"], linestyle=":", linewidth=2, label=r"$10^{-6}$ 精度线")

    ax.set_title("误差-步长双对数图", fontsize=16, weight="bold")
    ax.set_xlabel("步长 h")
    ax.set_ylabel("绝对误差 |E|")
    ax.grid(True, which="both", alpha=0.28)
    ax.legend()
    savefig(ASSET_DIR / "convergence.png")


def make_error_bar_chart():
    fig, ax = plt.subplots(figsize=(7.2, 4.2))

    x = np.arange(len(n_list))
    width = 0.34

    ax.bar(x - width / 2, err_Tn, width, color=C["orange"], label="复化梯形")
    ax.bar(x + width / 2, err_Sn, width, color=C["purple"], label="复化辛普森")

    ax.set_yscale("log")
    ax.axhline(tol, color=C["red"], linestyle="--", linewidth=2, label=r"$10^{-6}$")
    ax.set_xticks(x)
    ax.set_xticklabels([str(n) for n in n_list])
    ax.set_xlabel("等分数 n")
    ax.set_ylabel("绝对误差 |E|")
    ax.set_title("误差柱状对比", fontsize=16, weight="bold")
    ax.grid(axis="y", which="both", alpha=0.25)
    ax.legend()
    savefig(ASSET_DIR / "error_bar.png")


def make_ratio_chart():
    ratio_T = err_Tn[1:] / err_Tn[:-1]
    ratio_S = err_Sn[1:] / err_Sn[:-1]

    labels = [f"{n_list[i]}→{n_list[i+1]}" for i in range(len(n_list) - 1)]

    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    ax.plot(labels, ratio_T, "o-", color=C["orange"], linewidth=2.5, label="复化梯形")
    ax.plot(labels, ratio_S, "s-", color=C["purple"], linewidth=2.5, label="复化辛普森")

    ax.axhline(1 / 4, color=C["orange"], linestyle="--", alpha=0.7, label="1/4")
    ax.axhline(1 / 16, color=C["purple"], linestyle="--", alpha=0.7, label="1/16")

    ax.set_yscale("log")
    ax.set_title("步长减半后的误差比例", fontsize=16, weight="bold")
    ax.set_xlabel("n 加密过程")
    ax.set_ylabel("新误差 / 旧误差")
    ax.grid(True, which="both", alpha=0.25)
    ax.legend()
    savefig(ASSET_DIR / "ratio.png")


def make_cost_chart():
    fig, ax = plt.subplots(figsize=(7.2, 4.2))

    eval_T = n_list + 1
    eval_S = n_list + 1

    ax.plot(eval_T, err_Tn, "o-", color=C["orange"], linewidth=2.5, label="复化梯形")
    ax.plot(eval_S, err_Sn, "s-", color=C["purple"], linewidth=2.5, label="复化辛普森")

    ax.scatter([2], [err_T_single], color=C["red"], marker="X", s=120, label="普通梯形")
    ax.scatter([3], [err_S_single], color=C["blue"], marker="D", s=95, label="普通辛普森")

    ax.axhline(tol, color=C["red"], linestyle="--", linewidth=2, label=r"$10^{-6}$")

    ax.set_xscale("log", base=2)
    ax.set_yscale("log")
    ax.set_xlabel("函数估值次数")
    ax.set_ylabel("绝对误差 |E|")
    ax.set_title("计算量-精度对比", fontsize=16, weight="bold")
    ax.grid(True, which="both", alpha=0.25)
    ax.legend(fontsize=9)

    ax.annotate(
        "复化辛普森\nn=8 已达标",
        xy=(9, err_Sn[2]),
        xytext=(13, err_Sn[2] * 80),
        arrowprops=dict(arrowstyle="->", color=C["purple"], lw=1.6),
        fontsize=11,
        color=C["purple"]
    )

    savefig(ASSET_DIR / "cost.png")


def make_all_charts():
    make_curve_area_chart()
    make_trap_chart()
    make_simpson_chart()
    make_grid_chart()
    make_convergence_chart()
    make_error_bar_chart()
    make_ratio_chart()
    make_cost_chart()


# =========================
# 4. PPT 辅助函数
# =========================

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

blank = prs.slide_layouts[6]


def set_bg(slide, color=C["light"]):
    shape = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        0,
        0,
        prs.slide_width,
        prs.slide_height
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = rgb(color)
    shape.line.color.rgb = rgb(color)


def add_text(
    slide,
    text,
    x,
    y,
    w,
    h,
    size=18,
    color=C["black"],
    bold=False,
    align=PP_ALIGN.LEFT,
    valign=MSO_ANCHOR.TOP
):
    box = slide.shapes.add_textbox(
        Inches(x),
        Inches(y),
        Inches(w),
        Inches(h)
    )
    tf = box.text_frame
    tf.clear()
    tf.word_wrap = True
    tf.vertical_anchor = valign
    tf.margin_left = Inches(0.05)
    tf.margin_right = Inches(0.05)
    tf.margin_top = Inches(0.03)
    tf.margin_bottom = Inches(0.03)

    lines = str(text).split("\n")
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = line
        p.alignment = align
        p.font.name = FONT
        p.font.size = Pt(size)
        p.font.bold = bold
        p.font.color.rgb = rgb(color)
    return box


def add_title(slide, title, subtitle=None, dark=False):
    title_color = C["white"] if dark else C["navy"]
    sub_color = "#DCEEFF" if dark else C["gray"]

    add_text(
        slide,
        title,
        0.55,
        0.25,
        8.5,
        0.45,
        size=26,
        color=title_color,
        bold=True
    )

    line = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        Inches(0.58),
        Inches(0.82),
        Inches(1.25),
        Inches(0.06)
    )
    line.fill.solid()
    line.fill.fore_color.rgb = rgb(C["cyan"])
    line.line.color.rgb = rgb(C["cyan"])

    if subtitle:
        add_text(
            slide,
            subtitle,
            2.0,
            0.67,
            8.5,
            0.32,
            size=11,
            color=sub_color
        )


def add_footer(slide, page_no, dark=False):
    color = "#BFD7EA" if dark else C["gray"]
    add_text(
        slide,
        f"{page_no}",
        12.35,
        7.08,
        0.45,
        0.25,
        size=9,
        color=color,
        align=PP_ALIGN.RIGHT
    )


def add_round_rect(
    slide,
    x,
    y,
    w,
    h,
    fill=C["white"],
    line=C["blue"],
    radius=True
):
    shape_type = MSO_SHAPE.ROUNDED_RECTANGLE if radius else MSO_SHAPE.RECTANGLE
    shp = slide.shapes.add_shape(
        shape_type,
        Inches(x),
        Inches(y),
        Inches(w),
        Inches(h)
    )
    shp.fill.solid()
    shp.fill.fore_color.rgb = rgb(fill)
    shp.line.color.rgb = rgb(line)
    shp.line.width = Pt(1.1)
    return shp


def add_tag(slide, text, x, y, w, color=C["blue"]):
    add_round_rect(slide, x, y, w, 0.36, fill=color, line=color)
    add_text(
        slide,
        text,
        x + 0.04,
        y + 0.06,
        w - 0.08,
        0.24,
        size=10,
        color=C["white"],
        bold=True,
        align=PP_ALIGN.CENTER,
        valign=MSO_ANCHOR.MIDDLE
    )


def add_card(
    slide,
    x,
    y,
    w,
    h,
    title,
    value,
    fill=C["white"],
    accent=C["blue"],
    title_size=12,
    value_size=18
):
    add_round_rect(slide, x, y, w, h, fill=fill, line="#D8E2EF")

    stripe = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        Inches(x),
        Inches(y),
        Inches(0.08),
        Inches(h)
    )
    stripe.fill.solid()
    stripe.fill.fore_color.rgb = rgb(accent)
    stripe.line.color.rgb = rgb(accent)

    add_text(
        slide,
        title,
        x + 0.18,
        y + 0.12,
        w - 0.3,
        0.28,
        size=title_size,
        color=C["gray"],
        bold=True
    )

    add_text(
        slide,
        value,
        x + 0.18,
        y + 0.45,
        w - 0.3,
        h - 0.55,
        size=value_size,
        color=C["navy"],
        bold=True,
        valign=MSO_ANCHOR.MIDDLE
    )


def add_table(slide, data, x, y, w, h, font_size=10, header_fill=C["blue"]):
    rows = len(data)
    cols = len(data[0])

    shape = slide.shapes.add_table(
        rows,
        cols,
        Inches(x),
        Inches(y),
        Inches(w),
        Inches(h)
    )
    table = shape.table

    for r in range(rows):
        for c in range(cols):
            cell = table.cell(r, c)
            cell.text = str(data[r][c])
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            cell.margin_left = Inches(0.03)
            cell.margin_right = Inches(0.03)
            cell.margin_top = Inches(0.02)
            cell.margin_bottom = Inches(0.02)

            cell.fill.solid()
            if r == 0:
                cell.fill.fore_color.rgb = rgb(header_fill)
                font_color = C["white"]
                bold = True
                size = font_size + 1
            else:
                cell.fill.fore_color.rgb = rgb(C["white"] if r % 2 else C["table_alt"])
                font_color = C["black"]
                bold = False
                size = font_size

            for p in cell.text_frame.paragraphs:
                p.alignment = PP_ALIGN.CENTER
                p.font.name = FONT
                p.font.size = Pt(size)
                p.font.bold = bold
                p.font.color.rgb = rgb(font_color)

    return shape


def add_picture(slide, img_path, x, y, w, h):
    slide.shapes.add_picture(
        str(img_path),
        Inches(x),
        Inches(y),
        Inches(w),
        Inches(h)
    )


# =========================
# 5. 制作 PPT
# =========================

def build_ppt():
    make_all_charts()

    # ---------- Slide 1 封面 ----------
    slide = prs.slides.add_slide(blank)
    set_bg(slide, C["navy"])

    add_text(
        slide,
        "数值积分算法设计与实现",
        0.75,
        1.35,
        11.6,
        0.7,
        size=38,
        color=C["white"],
        bold=True,
        align=PP_ALIGN.CENTER
    )

    add_text(
        slide,
        "梯形公式 · 辛普森公式 · 复化求积",
        1.4,
        2.22,
        10.5,
        0.45,
        size=21,
        color="#DCEEFF",
        bold=True,
        align=PP_ALIGN.CENTER
    )

    add_tag(slide, "多图", 3.35, 3.05, 1.1, C["cyan"])
    add_tag(slide, "多表", 4.75, 3.05, 1.1, C["teal"])
    add_tag(slide, "少文字", 6.15, 3.05, 1.25, C["orange"])
    add_tag(slide, "Python自动生成", 7.65, 3.05, 1.85, C["purple"])

    add_text(
        slide,
        "工程背景：非线性变速运动位移积分\n"
        "速度函数：v(t)=4/(1+t²)，区间：[0,1]",
        2.3,
        4.15,
        8.8,
        0.7,
        size=16,
        color="#EAF6FF",
        align=PP_ALIGN.CENTER
    )

    add_text(
        slide,
        "团队：吴瑞东、余耽阳、饶宇佳、刘家乐、周亚辉",
        2.2,
        6.25,
        8.9,
        0.35,
        size=14,
        color="#BFD7EA",
        align=PP_ALIGN.CENTER
    )
    add_footer(slide, 1, dark=True)

    # ---------- Slide 2 团队分工 ----------
    slide = prs.slides.add_slide(blank)
    set_bg(slide)
    add_title(slide, "团队分工", "任务拆分清晰：推导、编程、结果、误差分析与汇报")

    team_data = [
        ["角色", "姓名", "主要负责内容"],
        ["组长", "吴瑞东", "思考题1-5、实验报告、讲解PPT"],
        ["组员", "余耽阳", "梯形与复化梯形：推导、代码、计算"],
        ["组员", "饶宇佳", "辛普森公式：推导、代码、计算"],
        ["组员", "刘家乐", "复化辛普森公式：推导、代码、计算"],
        ["组员", "周亚辉", "数据汇总、误差分析、图表绘制、PPT讲解"],
    ]
    add_table(slide, team_data, 0.85, 1.35, 11.65, 4.75, font_size=13)

    add_card(slide, 1.05, 6.35, 2.2, 0.65, "报告结构", "原理 → 实现 → 误差", accent=C["cyan"], value_size=13)
    add_card(slide, 3.55, 6.35, 2.2, 0.65, "核心对象", "∫₀¹ 4/(1+t²)dt", accent=C["teal"], value_size=13)
    add_card(slide, 6.05, 6.35, 2.2, 0.65, "精确值", "π", accent=C["orange"], value_size=18)
    add_card(slide, 8.55, 6.35, 2.2, 0.65, "重点对比", "精度 / 收敛 / 计算量", accent=C["purple"], value_size=12)
    add_footer(slide, 2)

    # ---------- Slide 3 实验目的 ----------
    slide = prs.slides.add_slide(blank)
    set_bg(slide)
    add_title(slide, "实验目的", "把连续定积分转化为离散加权求和")

    goals = [
        ("01", "数值积分思想", "连续积分\n→ 离散加权求和", C["blue"]),
        ("02", "公式推导", "梯形 / 辛普森\n误差特性", C["purple"]),
        ("03", "复化方法", "步长 h\n影响精度", C["teal"]),
        ("04", "编程实现", "四种算法\n统一比较", C["orange"]),
        ("05", "工程分析", "精度、稳定性\n计算成本", C["red"]),
    ]

    positions = [
        (0.85, 1.45), (4.7, 1.45), (8.55, 1.45),
        (2.75, 4.15), (6.65, 4.15)
    ]

    for (num, title, value, color), (x, y) in zip(goals, positions):
        add_round_rect(slide, x, y, 3.2, 1.75, fill=C["white"], line="#D8E2EF")
        add_text(slide, num, x + 0.15, y + 0.12, 0.55, 0.4, size=19, color=color, bold=True)
        add_text(slide, title, x + 0.75, y + 0.17, 2.2, 0.35, size=15, color=C["navy"], bold=True)
        add_text(slide, value, x + 0.35, y + 0.78, 2.55, 0.7, size=16, color=C["black"],
                 bold=True, align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)

    add_footer(slide, 3)

    # ---------- Slide 4 工程背景 ----------
    slide = prs.slides.add_slide(blank)
    set_bg(slide)
    add_title(slide, "工程背景", "工程中大量函数无法直接求原函数，需要数值积分")

    flow = [
        ("物理过程", "速度 / 热流 / 电量", C["blue"]),
        ("离散数据", "传感器 / 仿真 / 黑箱模型", C["teal"]),
        ("数值积分", "加权求和近似", C["orange"]),
        ("工程决策", "位移 / 能量 / 轨迹", C["purple"]),
    ]

    x0 = 0.75
    for i, (title, sub, color) in enumerate(flow):
        x = x0 + i * 3.05
        add_round_rect(slide, x, 1.35, 2.35, 1.25, fill=C["white"], line=color)
        add_text(slide, title, x + 0.1, 1.55, 2.15, 0.35, size=16, color=color, bold=True, align=PP_ALIGN.CENTER)
        add_text(slide, sub, x + 0.15, 2.02, 2.05, 0.35, size=11, color=C["black"], align=PP_ALIGN.CENTER)

        if i < 3:
            arrow = slide.shapes.add_shape(
                MSO_SHAPE.RIGHT_ARROW,
                Inches(x + 2.42),
                Inches(1.72),
                Inches(0.55),
                Inches(0.45)
            )
            arrow.fill.solid()
            arrow.fill.fore_color.rgb = rgb("#BFD7EA")
            arrow.line.color.rgb = rgb("#BFD7EA")

    examples = [
        ["领域", "典型积分任务"],
        ["航空航天", "再入热流密度积分 → 总热量"],
        ["车辆工程", "电池电流积分 → 剩余电量"],
        ["机器人控制", "速度积分 → 位移轨迹"],
        ["能源动力", "功率积分 → 能量消耗"],
    ]
    add_table(slide, examples, 1.25, 3.35, 10.8, 2.8, font_size=12, header_fill=C["teal"])

    add_footer(slide, 4)

    # ---------- Slide 5 模型与精确解 ----------
    slide = prs.slides.add_slide(blank)
    set_bg(slide)
    add_title(slide, "工程模型：滑块非线性变速运动", "位移 = 速度函数在时间区间上的定积分")

    add_picture(slide, ASSET_DIR / "curve_area.png", 0.75, 1.25, 6.9, 4.45)

    add_card(slide, 8.0, 1.45, 3.9, 0.95, "速度函数", "v(t)=4/(1+t²)", accent=C["blue"], value_size=21)
    add_card(slide, 8.0, 2.7, 3.9, 0.95, "积分区间", "[0,1] 秒", accent=C["teal"], value_size=21)
    add_card(slide, 8.0, 3.95, 3.9, 0.95, "精确位移", "S=π≈3.1415926536", accent=C["orange"], value_size=16)
    add_card(slide, 8.0, 5.2, 3.9, 0.95, "比较指标", "绝对误差 |I-Iₙ|", accent=C["purple"], value_size=17)

    add_footer(slide, 5)

    # ---------- Slide 6 方法总览 ----------
    slide = prs.slides.add_slide(blank)
    set_bg(slide)
    add_title(slide, "四种算法总览", "普通公式用于单区间；复化公式通过加密网格提升精度")

    alg_data = [
        ["算法", "核心思想", "函数估值", "误差阶", "限制"],
        ["普通梯形", "端点直线", "2", "局部 O(h³)", "粗略估算"],
        ["普通辛普森", "三点抛物线", "3", "局部 O(h⁵)", "函数光滑"],
        ["复化梯形", "分段梯形累加", "n+1", "整体 O(h²)", "n 任意"],
        ["复化辛普森", "两段一组抛物线", "n+1", "整体 O(h⁴)", "n 必须为偶数"],
    ]
    add_table(slide, alg_data, 0.75, 1.25, 11.85, 3.4, font_size=12)

    add_card(slide, 1.05, 5.25, 2.55, 0.8, "低成本", "普通公式", accent=C["gray"], value_size=18)
    add_card(slide, 3.9, 5.25, 2.55, 0.8, "可收敛", "复化公式", accent=C["cyan"], value_size=18)
    add_card(slide, 6.75, 5.25, 2.55, 0.8, "高精度", "辛普森", accent=C["purple"], value_size=18)
    add_card(slide, 9.6, 5.25, 2.55, 0.8, "工程首选", "复化辛普森", accent=C["orange"], value_size=16)

    add_footer(slide, 6)

    # ---------- Slide 7 梯形公式 ----------
    slide = prs.slides.add_slide(blank)
    set_bg(slide)
    add_title(slide, "梯形求积公式", "用端点连线近似曲线下方面积")

    add_picture(slide, ASSET_DIR / "trap.png", 0.7, 1.35, 6.95, 4.4)

    add_card(slide, 8.0, 1.35, 4.0, 0.85, "普通梯形公式", "T=(b-a)[f(a)+f(b)]/2", accent=C["orange"], value_size=14)
    add_card(slide, 8.0, 2.45, 4.0, 0.85, "本题结果", f"T={fmt_num(T_single, 6)}", accent=C["blue"], value_size=20)
    add_card(slide, 8.0, 3.55, 4.0, 0.85, "绝对误差", fmt_err(err_T_single), accent=C["red"], value_size=20)
    add_card(slide, 8.0, 4.65, 4.0, 0.85, "特点", "简单，但精度低", accent=C["gray"], value_size=18)

    add_footer(slide, 7)

    # ---------- Slide 8 辛普森公式 ----------
    slide = prs.slides.add_slide(blank)
    set_bg(slide)
    add_title(slide, "辛普森公式", "用端点与中点确定抛物线，近似曲边面积")

    add_picture(slide, ASSET_DIR / "simpson.png", 0.7, 1.35, 6.95, 4.4)

    add_card(slide, 8.0, 1.35, 4.0, 0.85, "辛普森公式", "S=(b-a)[f(a)+4f(m)+f(b)]/6", accent=C["purple"], value_size=12)
    add_card(slide, 8.0, 2.45, 4.0, 0.85, "本题结果", f"S={fmt_num(S_single, 6)}", accent=C["blue"], value_size=20)
    add_card(slide, 8.0, 3.55, 4.0, 0.85, "绝对误差", fmt_err(err_S_single), accent=C["red"], value_size=20)
    add_card(slide, 8.0, 4.65, 4.0, 0.85, "代数精度", "三次多项式精确", accent=C["teal"], value_size=17)

    add_footer(slide, 8)

    # ---------- Slide 9 复化求积 ----------
    slide = prs.slides.add_slide(blank)
    set_bg(slide)
    add_title(slide, "复化求积思想", "把区间细分，逐段近似，再累加")

    add_picture(slide, ASSET_DIR / "grid.png", 0.7, 1.25, 6.75, 4.2)

    comp_data = [
        ["方法", "离散公式核心", "误差阶"],
        ["复化梯形", "h[0.5f₀+Σfᵢ+0.5fₙ]", "O(h²)"],
        ["复化辛普森", "h/3[f₀+4Σf奇+2Σf偶+fₙ]", "O(h⁴)"],
    ]
    add_table(slide, comp_data, 7.75, 1.35, 4.65, 1.95, font_size=10, header_fill=C["purple"])

    add_card(slide, 7.9, 3.75, 2.0, 0.8, "步长", "h=(b-a)/n", accent=C["cyan"], value_size=15)
    add_card(slide, 10.15, 3.75, 2.0, 0.8, "节点", "xᵢ=a+ih", accent=C["teal"], value_size=15)
    add_card(slide, 7.9, 4.8, 4.25, 0.85, "辛普森约束", "n 必须为偶数", accent=C["red"], value_size=18)

    add_footer(slide, 9)

    # ---------- Slide 10 算法实现 ----------
    slide = prs.slides.add_slide(blank)
    set_bg(slide)
    add_title(slide, "算法实现", "四个函数：输入 f,a,b,n，输出近似积分值")

    code_data = [
        ["函数", "核心计算", "说明"],
        ["trapezoid_single", "(b-a)(f(a)+f(b))/2", "普通梯形"],
        ["simpson_single", "(b-a)(f(a)+4f(m)+f(b))/6", "普通辛普森"],
        ["composite_trapezoid", "h(0.5f₀+Σfᵢ+0.5fₙ)", "n 任意"],
        ["composite_simpson", "h/3(f₀+4Σf奇+2Σf偶+fₙ)", "n 为偶数"],
    ]
    add_table(slide, code_data, 0.75, 1.3, 11.85, 3.2, font_size=11, header_fill=C["blue"])

    add_card(slide, 1.0, 5.1, 2.5, 0.8, "输入", "f, a, b, n", accent=C["blue"], value_size=18)
    add_card(slide, 3.9, 5.1, 2.5, 0.8, "过程", "节点 → 权重 → 求和", accent=C["teal"], value_size=14)
    add_card(slide, 6.8, 5.1, 2.5, 0.8, "输出", "Iₙ", accent=C["orange"], value_size=21)
    add_card(slide, 9.7, 5.1, 2.5, 0.8, "评价", "|I-Iₙ|", accent=C["red"], value_size=21)

    add_footer(slide, 10)

    # ---------- Slide 11 实验结果表 ----------
    slide = prs.slides.add_slide(blank)
    set_bg(slide)
    add_title(slide, "实验结果汇总", "被积函数：v(t)=4/(1+t²)，精确值：π")

    result_data = [["方法", "n", "h", "近似积分值", "绝对误差"]]
    result_data.append(["普通梯形", "1", "1.000000", fmt_num(T_single, 12), fmt_err(err_T_single)])
    result_data.append(["普通辛普森", "1", "1.000000", fmt_num(S_single, 12), fmt_err(err_S_single)])

    for n, h, val, err in zip(n_list, h_list, Tn, err_Tn):
        result_data.append(["复化梯形", str(int(n)), f"{h:.6f}", fmt_num(val, 12), fmt_err(err)])

    for n, h, val, err in zip(n_list, h_list, Sn, err_Sn):
        result_data.append(["复化辛普森", str(int(n)), f"{h:.6f}", fmt_num(val, 12), fmt_err(err)])

    add_table(slide, result_data, 0.55, 1.15, 12.25, 5.85, font_size=8, header_fill=C["teal"])
    add_footer(slide, 11)

    # ---------- Slide 12 误差对比 ----------
    slide = prs.slides.add_slide(blank)
    set_bg(slide)
    add_title(slide, "误差对比", "复化辛普森误差下降最快")

    add_picture(slide, ASSET_DIR / "error_bar.png", 6.65, 1.3, 5.95, 4.1)

    err_table = [
        ["方法", "代表误差"],
        ["普通梯形", fmt_err(err_T_single)],
        ["普通辛普森", fmt_err(err_S_single)],
        ["复化梯形 n=64", fmt_err(err_Tn[-1])],
        ["复化辛普森 n=8", fmt_err(err_Sn[2])],
        ["复化辛普森 n=64", fmt_err(err_Sn[-1])],
    ]
    add_table(slide, err_table, 0.85, 1.4, 5.1, 3.2, font_size=12, header_fill=C["orange"])

    add_card(slide, 0.95, 5.15, 2.35, 0.85, "误差最大", "普通梯形", accent=C["red"], value_size=17)
    add_card(slide, 3.6, 5.15, 2.35, 0.85, "收敛最快", "复化辛普森", accent=C["purple"], value_size=15)

    add_footer(slide, 12)

    # ---------- Slide 13 误差-步长 ----------
    slide = prs.slides.add_slide(blank)
    set_bg(slide)
    add_title(slide, "误差-步长关系", "双对数图可以直观看出收敛阶")

    add_picture(slide, ASSET_DIR / "convergence.png", 0.7, 1.15, 7.15, 4.65)

    add_card(slide, 8.25, 1.35, 3.5, 0.8, "复化梯形", "误差约 O(h²)", accent=C["orange"], value_size=18)
    add_card(slide, 8.25, 2.45, 3.5, 0.8, "复化辛普森", "误差约 O(h⁴)", accent=C["purple"], value_size=18)
    add_card(slide, 8.25, 3.55, 3.5, 0.8, "步长减半", "梯形约降为 1/4", accent=C["teal"], value_size=15)
    add_card(slide, 8.25, 4.65, 3.5, 0.8, "步长减半", "辛普森约降为 1/16", accent=C["blue"], value_size=14)

    add_footer(slide, 13)

    # ---------- Slide 14 收敛阶验证 ----------
    slide = prs.slides.add_slide(blank)
    set_bg(slide)
    add_title(slide, "收敛阶验证", "观察步长减半后的误差比例")

    add_picture(slide, ASSET_DIR / "ratio.png", 0.75, 1.25, 6.7, 4.25)

    ratio_T = err_Tn[1:] / err_Tn[:-1]
    ratio_S = err_Sn[1:] / err_Sn[:-1]
    ratio_data = [["n变化", "梯形误差比", "辛普森误差比"]]
    for i in range(len(ratio_T)):
        ratio_data.append([
            f"{n_list[i]}→{n_list[i+1]}",
            f"{ratio_T[i]:.3e}",
            f"{ratio_S[i]:.3e}",
        ])

    add_table(slide, ratio_data, 7.75, 1.35, 4.5, 3.6, font_size=9, header_fill=C["purple"])
    add_card(slide, 8.0, 5.35, 4.0, 0.75, "结论", "复化辛普森收敛显著更快", accent=C["red"], value_size=15)

    add_footer(slide, 14)

    # ---------- Slide 15 计算量-精度 ----------
    slide = prs.slides.add_slide(blank)
    set_bg(slide)
    add_title(slide, "计算量-精度对比", "同样精度下，复化辛普森所需函数估值更少")

    add_picture(slide, ASSET_DIR / "cost.png", 0.75, 1.25, 6.75, 4.25)

    target_data = [
        ["算法", "达到 10⁻⁶ 精度所需 n"],
        ["普通梯形", "无法达到"],
        ["普通辛普森", "无法达到"],
        ["复化梯形", f"最小 n={min_n_trap}；常取 {next_pow2_trap}"],
        ["复化辛普森", f"最小 n={min_n_simp}"],
    ]
    add_table(slide, target_data, 7.8, 1.35, 4.55, 2.75, font_size=10, header_fill=C["teal"])

    add_card(slide, 7.9, 4.65, 2.05, 0.8, "高精度", "辛普森", accent=C["purple"], value_size=18)
    add_card(slide, 10.2, 4.65, 2.05, 0.8, "低成本", "少量节点", accent=C["orange"], value_size=17)

    add_footer(slide, 15)

    # ---------- Slide 16 工程应用建议 ----------
    slide = prs.slides.add_slide(blank)
    set_bg(slide)
    add_title(slide, "工程应用选择建议", "根据函数光滑性、精度要求和计算资源选择算法")

    app_data = [
        ["工程场景", "建议算法", "原因"],
        ["实时嵌入式系统", "复化辛普森 n=4/8", "高精度、低计算量"],
        ["大规模仿真 CFD/FEM", "复化辛普森", "收敛快，减少总耗时"],
        ["实验离散数据", "辛普森或梯形", "视采样点数量而定"],
        ["函数不光滑", "复化梯形", "更稳健，避免辛普森降阶"],
        ["黑箱/昂贵模型", "传统积分 + 代理模型", "需交叉验证"],
    ]
    add_table(slide, app_data, 0.7, 1.25, 11.95, 4.35, font_size=11, header_fill=C["blue"])

    add_card(slide, 1.05, 6.05, 2.5, 0.75, "首选", "复化辛普森", accent=C["purple"], value_size=16)
    add_card(slide, 3.95, 6.05, 2.5, 0.75, "稳健", "复化梯形", accent=C["orange"], value_size=16)
    add_card(slide, 6.85, 6.05, 2.5, 0.75, "粗略", "普通公式", accent=C["gray"], value_size=16)
    add_card(slide, 9.75, 6.05, 2.5, 0.75, "关键", "误差阶指导 h", accent=C["teal"], value_size=15)

    add_footer(slide, 16)

    # ---------- Slide 17 思考题精选 ----------
    slide = prs.slides.add_slide(blank)
    set_bg(slide)
    add_title(slide, "思考题精选", "用关键词回答，便于汇报讲解")

    cards = [
        ("1. 辛普森为何三次精确？", "三次多项式 f⁽⁴⁾=0\n截断误差为 0", C["purple"]),
        ("2. 两种复化误差阶为何不同？", "插值阶不同\n梯形 O(h²)，辛普森 O(h⁴)", C["orange"]),
        ("3. 线性性工程意义？", "复杂速度分量\n可分别积分再叠加", C["teal"]),
        ("4. 机器学习积分优缺点？", "预测快\n但误差界弱、可解释性弱", C["red"]),
        ("5. 误差阶有什么作用？", "预测所需 n\n控制精度与成本", C["blue"]),
    ]

    pos = [
        (0.75, 1.35), (4.75, 1.35), (8.75, 1.35),
        (2.75, 4.15), (6.75, 4.15)
    ]

    for (title, value, color), (x, y) in zip(cards, pos):
        add_round_rect(slide, x, y, 3.25, 1.65, fill=C["white"], line=color)
        add_text(slide, title, x + 0.18, y + 0.18, 2.9, 0.42, size=12, color=color, bold=True)
        add_text(slide, value, x + 0.2, y + 0.72, 2.85, 0.65, size=14, color=C["navy"],
                 bold=True, align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)

    add_footer(slide, 17)

    # ---------- Slide 18 总结 ----------
    slide = prs.slides.add_slide(blank)
    set_bg(slide, C["navy"])
    add_title(slide, "总结", "对于光滑函数，复化辛普森是精度与效率兼顾的首选", dark=True)

    add_card(slide, 1.05, 1.45, 3.25, 1.2, "结论 1", "复化公式可通过减小 h 提高精度", fill="#13213F", accent=C["cyan"], value_size=16)
    add_card(slide, 5.05, 1.45, 3.25, 1.2, "结论 2", "复化辛普森收敛速度最快", fill="#13213F", accent=C["purple"], value_size=17)
    add_card(slide, 9.05, 1.45, 3.25, 1.2, "结论 3", "误差阶直接指导步长选择", fill="#13213F", accent=C["orange"], value_size=16)

    rank_data = [
        ["综合表现", "算法"],
        ["★★★★★", "复化辛普森"],
        ["★★★☆☆", "复化梯形"],
        ["★★☆☆☆", "普通辛普森"],
        ["★☆☆☆☆", "普通梯形"],
    ]
    add_table(slide, rank_data, 3.3, 3.25, 6.7, 2.25, font_size=13, header_fill=C["purple"])

    add_text(
        slide,
        "THANKS  /  Q&A",
        4.1,
        6.25,
        5.2,
        0.5,
        size=28,
        color=C["white"],
        bold=True,
        align=PP_ALIGN.CENTER
    )
    add_footer(slide, 18, dark=True)

    prs.save(OUT_FILE)


if __name__ == "__main__":
    build_ppt()
    print(f"已生成 PPT：{OUT_FILE}")
    print(f"图片素材目录：{ASSET_DIR.resolve()}")