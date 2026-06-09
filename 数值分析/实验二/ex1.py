import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import RBFInterpolator
import os
import warnings
warnings.filterwarnings('ignore')

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 获取脚本所在目录
script_dir = os.path.dirname(os.path.abspath(__file__))

# 读取数据
df_true = pd.read_excel(os.path.join(script_dir, 'true.xlsx'))
df_A = pd.read_excel(os.path.join(script_dir, '模式A.xlsx'))
df_B = pd.read_excel(os.path.join(script_dir, '模式B.xlsx'))

# 按日期排序（从早到晚）
df_true = df_true.sort_values('交易日期').reset_index(drop=True)
df_A = df_A.sort_values('交易日期').reset_index(drop=True)
df_B = df_B.sort_values('交易日期').reset_index(drop=True)

# 创建索引（用行号作为RBF插值的输入）
dates = df_true['交易日期']
true_prices = df_true['收盘价'].values

# 模式A插值
mask_A = df_A['收盘价'].notna()
known_idx_A = np.where(mask_A)[0].reshape(-1, 1)
known_prices_A = df_A.loc[mask_A, '收盘价'].values

# RBF插值 - 模式A
all_idx_A = np.arange(len(df_A)).reshape(-1, 1)
rbf_A = RBFInterpolator(known_idx_A.astype(float), known_prices_A, kernel='thin_plate_spline')
interpolated_A = rbf_A(all_idx_A.astype(float))

# 模式B插值
mask_B = df_B['收盘价'].notna()
known_idx_B = np.where(mask_B)[0].reshape(-1, 1)
known_prices_B = df_B.loc[mask_B, '收盘价'].values

# RBF插值 - 模式B
all_idx_B = np.arange(len(df_B)).reshape(-1, 1)
rbf_B = RBFInterpolator(known_idx_B.astype(float), known_prices_B, kernel='thin_plate_spline')
interpolated_B = rbf_B(all_idx_B.astype(float))

# 计算5日均线
ma5_true = pd.Series(true_prices).rolling(window=5).mean().values
ma5_A = pd.Series(interpolated_A).rolling(window=5).mean().values
ma5_B = pd.Series(interpolated_B).rolling(window=5).mean().values

# 计算误差指标（RMSE和MAE）
rmse_A = np.sqrt(np.mean((true_prices - interpolated_A) ** 2))
mae_A = np.mean(np.abs(true_prices - interpolated_A))
rmse_B = np.sqrt(np.mean((true_prices - interpolated_B) ** 2))
mae_B = np.mean(np.abs(true_prices - interpolated_B))

# 误差表格
print("=" * 50)
print("误差指标表格")
print("=" * 50)
print(f"{'模式':<10} {'RMSE':<15} {'MAE':<15}")
print("-" * 50)
print(f"{'模式A':<10} {rmse_A:<15.4f} {mae_A:<15.4f}")
print(f"{'模式B':<10} {rmse_B:<15.4f} {mae_B:<15.4f}")
print("=" * 50)

# 计算均线与真实均线的最大偏离值（忽略NaN值）
valid_mask = ~(np.isnan(ma5_A) | np.isnan(ma5_true))
max_deviation_A = np.max(np.abs(ma5_A[valid_mask] - ma5_true[valid_mask]))

valid_mask_B = ~(np.isnan(ma5_B) | np.isnan(ma5_true))
max_deviation_B = np.max(np.abs(ma5_B[valid_mask_B] - ma5_true[valid_mask_B]))

# 计算信号滞后/超前天数
# 使用均线交叉信号：当价格上穿均线时为买入信号，下穿为卖出信号
def generate_signals(prices, ma5):
    signals = []
    for i in range(1, len(prices)):
        if prices[i-1] < ma5[i-1] and prices[i] > ma5[i]:
            signals.append(('买入', i))
        elif prices[i-1] > ma5[i-1] and prices[i] < ma5[i]:
            signals.append(('卖出', i))
    return signals

signals_true = generate_signals(true_prices, ma5_true)
signals_A = generate_signals(interpolated_A, ma5_A)
signals_B = generate_signals(interpolated_B, ma5_B)

# 信号对比
def compare_signals(signals_true, signals_interp, name):
    print(f"\n{name} 信号差异分析:")
    print("-" * 60)
    
    if len(signals_true) == 0 or len(signals_interp) == 0:
        print("信号数量不足，无法对比")
        return []
    
    delays = []
    used_interp = set()
    
    for sig_type_true, idx_true in signals_true:
        closest_idx = None
        min_diff = float('inf')
        best_j = None
        
        for j, (sig_type_interp, idx_interp) in enumerate(signals_interp):
            if sig_type_interp == sig_type_true and j not in used_interp:
                diff = abs(idx_interp - idx_true)
                if diff < min_diff:
                    min_diff = diff
                    closest_idx = idx_interp
                    best_j = j
        
        if closest_idx is not None:
            used_interp.add(best_j)
            diff = closest_idx - idx_true
            delays.append(diff)
            if diff > 0:
                timing = f"滞后{diff}天"
            elif diff < 0:
                timing = f"超前{abs(diff)}天"
            else:
                timing = "同步"
            print(f"真实信号 {sig_type_true}(第{idx_true}天) -> {name}信号 {sig_type_true}(第{closest_idx}天): {timing}")
        else:
            print(f"真实信号 {sig_type_true}(第{idx_true}天) -> {name}: 无对应信号")
    
    return delays

delays_A = compare_signals(signals_true, signals_A, "模式A")
delays_B = compare_signals(signals_true, signals_B, "模式B")

# 信号差异表格
print("\n" + "=" * 70)
print("信号差异表格")
print("=" * 70)
print(f"{'模式':<10} {'最大偏离值':<15} {'信号数量':<10} {'平均滞后/超前天数':<20}")
print("-" * 70)

avg_delay_A = np.mean(delays_A) if len(delays_A) > 0 else 0
avg_delay_B = np.mean(delays_B) if len(delays_B) > 0 else 0

print(f"{'模式A':<10} {max_deviation_A:<15.4f} {len(signals_A):<10} {avg_delay_A:<20.2f}")
print(f"{'模式B':<10} {max_deviation_B:<15.4f} {len(signals_B):<10} {avg_delay_B:<20.2f}")
print("=" * 70)

# 绘制对比图
fig, axes = plt.subplots(3, 1, figsize=(14, 12))

# (a) 价格插值对比
axes[0].plot(dates, true_prices, 'k-', label='真实价格', linewidth=2, alpha=0.8)
axes[0].plot(dates, interpolated_A, 'r--', label='模式A插值', linewidth=1.5, alpha=0.7)
axes[0].plot(dates, interpolated_B, 'b-.', label='模式B插值', linewidth=1.5, alpha=0.7)

# 标记缺失点
missing_A = df_A['收盘价'].isna()
missing_B = df_B['收盘价'].isna()
axes[0].scatter(dates[missing_A], interpolated_A[missing_A], c='red', marker='x', s=50, label='模式A缺失点', alpha=0.6)
axes[0].scatter(dates[missing_B], interpolated_B[missing_B], c='blue', marker='x', s=50, label='模式B缺失点', alpha=0.6)

axes[0].set_title('(a) 价格插值对比', fontsize=14, fontweight='bold')
axes[0].set_ylabel('价格', fontsize=12)
axes[0].legend(fontsize=10)
axes[0].grid(True, alpha=0.3)
axes[0].tick_params(axis='x', rotation=45)

# (b) 5日均线对比 - 模式A
axes[1].plot(dates, ma5_true, 'k-', label='真实5日均线', linewidth=2, alpha=0.8)
axes[1].plot(dates, ma5_A, 'r--', label='模式A插值5日均线', linewidth=1.5, alpha=0.7)
axes[1].set_title('(b) 5日均线对比 - 模式A', fontsize=14, fontweight='bold')
axes[1].set_ylabel('5日均线', fontsize=12)
axes[1].legend(fontsize=10)
axes[1].grid(True, alpha=0.3)
axes[1].tick_params(axis='x', rotation=45)

# (b) 5日均线对比 - 模式B
axes[2].plot(dates, ma5_true, 'k-', label='真实5日均线', linewidth=2, alpha=0.8)
axes[2].plot(dates, ma5_B, 'b-.', label='模式B插值5日均线', linewidth=1.5, alpha=0.7)
axes[2].set_title('(b) 5日均线对比 - 模式B', fontsize=14, fontweight='bold')
axes[2].set_ylabel('5日均线', fontsize=12)
axes[2].set_xlabel('交易日期', fontsize=12)
axes[2].legend(fontsize=10)
axes[2].grid(True, alpha=0.3)
axes[2].tick_params(axis='x', rotation=45)

plt.tight_layout()
output_path = os.path.join(script_dir, 'RBF插值对比图.png')
plt.savefig(output_path, dpi=300, bbox_inches='tight')
plt.show()

print(f"\n图表已保存为 '{output_path}'")

# 保存插值后的数据到新文件
df_A_filled = df_A.copy()
df_A_filled['收盘价'] = interpolated_A
output_A_path = os.path.join(script_dir, '模式A_插值后.xlsx')
df_A_filled.to_excel(output_A_path, index=False)
print(f"模式A插值后数据已保存为 '{output_A_path}'")

df_B_filled = df_B.copy()
df_B_filled['收盘价'] = interpolated_B
output_B_path = os.path.join(script_dir, '模式B_插值后.xlsx')
df_B_filled.to_excel(output_B_path, index=False)
print(f"模式B插值后数据已保存为 '{output_B_path}'")
