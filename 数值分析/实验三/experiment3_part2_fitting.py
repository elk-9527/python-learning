# 实验三 Part2：最小二乘拟合 + 正则化对比 + 误差分析 + 轨迹排序 + 可视化
import os
os.environ['LOKY_MAX_CPU_COUNT'] = '4'
os.environ['OMP_NUM_THREADS'] = '1'
os.environ['OPENBLAS_NUM_THREADS'] = '1'
os.environ['MKL_NUM_THREADS'] = '1'
import logging
logging.basicConfig(level=logging.ERROR)
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression, Lasso
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import KFold
from scipy import stats
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

BASE_DIR = r'd:\documents\Python\数值分析\实验三\Datasets for P3\datasets'
DATASET = 'simulation'
LABEL_FILE = f'{BASE_DIR}/{DATASET}/cell_labels.xlsx'

# ============================================================
# 加载预处理结果
# ============================================================
print('=' * 60)
print('加载预处理数据')
print('=' * 60)

data = np.load(f'{BASE_DIR}/{DATASET}/preprocess_result.npz', allow_pickle=True)
norm_expr = data['norm_expr']
module_expr = data['module_expr']
all_sampled_cells = data['all_sampled_cells']
all_time_points = data['all_time_points']
all_branches = data['all_branches']
optimal_k = int(data['optimal_k'])
silhouette_scores = data['silhouette_scores']
k_range = data['k_range']

labels_df = pd.read_excel(LABEL_FILE, index_col=0, engine='calamine')
n_cells = norm_expr.shape[0]
n_genes = data['gene_cluster_labels'].shape[0]

print(f'模块数: {optimal_k}, 抽样细胞: {len(all_sampled_cells)}')
print(f'Left分支: {(all_branches == "Left").sum()}, Right分支: {(all_branches == "Right").sum()}')

# ============================================================
# 步骤4：最小二乘曲线拟合 —— 每条分支独立拟合
# ============================================================
print('\n' + '=' * 60)
print('步骤4：最小二乘曲线拟合 (分支独立)')
print('=' * 60)

degrees = [1, 2, 3]
lasso_lambdas = [0.001, 0.01, 0.1, 0.5, 1.0, 5.0]

branch_results = {}

for br_name in ['Left', 'Right']:
    br_mask = all_branches == br_name
    br_cells = all_sampled_cells[br_mask]
    br_times = all_time_points[br_mask]
    T_br = br_times.reshape(-1, 1)
    n_br = len(br_cells)

    print(f'\n--- {br_name} 分支 ({n_br} cells) ---')

    branch_fittings = {}
    for mod_id in range(optimal_k):
        y = module_expr[br_cells, mod_id]
        mod_results = {'degree': {}, 'lasso': {}}

        for deg in degrees:
            # include_bias=False + fit_intercept=True — 无重复全1列
            poly = PolynomialFeatures(degree=deg, include_bias=False)
            T_poly = poly.fit_transform(T_br)

            # OLS
            lr = LinearRegression()
            lr.fit(T_poly, y)
            y_pred = lr.predict(T_poly)
            r2 = r2_score(y, y_pred)
            rmse = np.sqrt(mean_squared_error(y, y_pred))
            mod_results['degree'][deg] = {'r2': r2, 'rmse': rmse, 'y_pred': y_pred}

            # Lasso 同阶正则化
            best_lasso_r2 = -np.inf
            best_lasso_rmse = np.inf
            best_lasso_lam = None
            best_lasso_pred = None
            for lam in lasso_lambdas:
                lasso = Lasso(alpha=lam, max_iter=10000, random_state=42)
                lasso.fit(T_poly, y)
                y_pred_l = lasso.predict(T_poly)
                r2_l = r2_score(y, y_pred_l)
                rmse_l = np.sqrt(mean_squared_error(y, y_pred_l))
                if r2_l > best_lasso_r2:
                    best_lasso_r2 = r2_l
                    best_lasso_rmse = rmse_l
                    best_lasso_lam = lam
                    best_lasso_pred = y_pred_l
            mod_results['lasso'][deg] = {'lambda': best_lasso_lam, 'r2': best_lasso_r2,
                                           'rmse': best_lasso_rmse, 'y_pred': best_lasso_pred}

        branch_fittings[mod_id] = mod_results
        best_ols = max(mod_results['degree'].items(), key=lambda x: x[1]['r2'])
        print(f'  模块 {mod_id}: OLS最佳deg={best_ols[0]}, R^2={best_ols[1]["r2"]:.4f}, '
              f'RMSE={best_ols[1]["rmse"]:.4f}')

    branch_results[br_name] = branch_fittings

# 使用 Left 分支数据做主要分析（两条分支对称，选一条即可；也可分别报告）
all_fitting_results = branch_results['Left']
# 同时保留 Right 分支结果用于对比
T_branch = {'Left': all_time_points[all_branches == 'Left'].reshape(-1, 1),
            'Right': all_time_points[all_branches == 'Right'].reshape(-1, 1)}
cells_branch = {'Left': all_sampled_cells[all_branches == 'Left'],
                'Right': all_sampled_cells[all_branches == 'Right']}

# ============================================================
# 5折交叉验证选择最优 λ (Left分支)
# ============================================================
print('\n' + '=' * 60)
print('步骤4.6：5折交叉验证选择 lambda (Left分支)')
print('=' * 60)

T_lf = T_branch['Left']
cells_lf = cells_branch['Left']

kf = KFold(n_splits=5, shuffle=True, random_state=42)
cv_results = {lam: [] for lam in lasso_lambdas}
cv_rmse_ols = []

for fold, (train_idx, val_idx) in enumerate(kf.split(T_lf)):
    T_train, T_val = T_lf[train_idx], T_lf[val_idx]
    cv_rmse_fold = []
    for mod_id in range(optimal_k):
        y_all = module_expr[cells_lf, mod_id]
        y_train, y_val = y_all[train_idx], y_all[val_idx]
        poly = PolynomialFeatures(degree=3, include_bias=False)
        Tp_train = poly.fit_transform(T_train)
        Tp_val = poly.transform(T_val)
        lr = LinearRegression().fit(Tp_train, y_train)
        y_pred_val = lr.predict(Tp_val)
        cv_rmse_fold.append(np.sqrt(mean_squared_error(y_val, y_pred_val)))
    cv_rmse_ols.append(np.mean(cv_rmse_fold))

    for lam in lasso_lambdas:
        cv_rmse_fold = []
        for mod_id in range(optimal_k):
            y_all = module_expr[cells_lf, mod_id]
            y_train, y_val = y_all[train_idx], y_all[val_idx]
            poly = PolynomialFeatures(degree=3, include_bias=False)
            Tp_train = poly.fit_transform(T_train)
            Tp_val = poly.transform(T_val)
            lasso = Lasso(alpha=lam, max_iter=10000, random_state=42).fit(Tp_train, y_train)
            y_pred_val = lasso.predict(Tp_val)
            cv_rmse_fold.append(np.sqrt(mean_squared_error(y_val, y_pred_val)))
        cv_results[lam].append(np.mean(cv_rmse_fold))

    print(f'  Fold {fold+1}: OLS RMSE={cv_rmse_ols[-1]:.4f}, '
          + ', '.join([f'lam={lam} RMSE={cv_results[lam][-1]:.4f}' for lam in lasso_lambdas[:3]]) + '...')

avg_cv_rmse_ols = np.mean(cv_rmse_ols)
avg_cv_rmse_lasso = {lam: np.mean(cv_results[lam]) for lam in lasso_lambdas}
best_lam_cv = min(avg_cv_rmse_lasso, key=avg_cv_rmse_lasso.get)

print(f'\n  OLS 平均CV-RMSE: {avg_cv_rmse_ols:.4f}')
for lam in lasso_lambdas:
    print(f'  Lasso lam={lam:.4f} 平均CV-RMSE: {avg_cv_rmse_lasso[lam]:.4f}')
print(f'  最优 lam = {best_lam_cv}')

# 用CV最优λ统一重新拟合Lasso（覆盖之前in-sample选λ的结果）
print('\n--- 用CV最优λ重新拟合Lasso ---')
for br_name in ['Left', 'Right']:
    br_mask = all_branches == br_name
    br_cells = all_sampled_cells[br_mask]
    br_times = all_time_points[br_mask]
    T_br = br_times.reshape(-1, 1)
    for mod_id in range(optimal_k):
        y = module_expr[br_cells, mod_id]
        for deg in degrees:
            poly = PolynomialFeatures(degree=deg, include_bias=False)
            T_poly = poly.fit_transform(T_br)
            lasso = Lasso(alpha=best_lam_cv, max_iter=10000, random_state=42)
            lasso.fit(T_poly, y)
            y_pred_l = lasso.predict(T_poly)
            r2_l = r2_score(y, y_pred_l)
            rmse_l = np.sqrt(mean_squared_error(y, y_pred_l))
            branch_results[br_name][mod_id]['lasso'][deg] = {
                'lambda': best_lam_cv, 'r2': r2_l, 'rmse': rmse_l, 'y_pred': y_pred_l
            }
print(f'  Lasso已用 lam={best_lam_cv} 重新拟合完成')

print('\n--- 同阶数 OLS vs Lasso 对比 (CV-λ修正后) ---')
for deg in degrees:
    avg_r2_ols = np.mean([all_fitting_results[m]['degree'][deg]['r2'] for m in range(optimal_k)])
    avg_rmse_ols = np.mean([all_fitting_results[m]['degree'][deg]['rmse'] for m in range(optimal_k)])
    avg_r2_lasso = np.mean([all_fitting_results[m]['lasso'][deg]['r2'] for m in range(optimal_k)])
    avg_rmse_lasso = np.mean([all_fitting_results[m]['lasso'][deg]['rmse'] for m in range(optimal_k)])
    print(f'  deg={deg}: OLS R^2={avg_r2_ols:.4f} RMSE={avg_rmse_ols:.4f} | '
          f'Lasso R^2={avg_r2_lasso:.4f} RMSE={avg_rmse_lasso:.4f}')

# ============================================================
# 步骤5：误差分析与假设检验
# ============================================================
print('\n' + '=' * 60)
print('步骤5：误差分析与假设检验')
print('=' * 60)

significant_modules = []
for mod_id in range(optimal_k):
    y = module_expr[cells_lf, mod_id]

    best_deg = max(all_fitting_results[mod_id]['degree'].items(), key=lambda x: x[1]['r2'])[0]
    poly = PolynomialFeatures(degree=best_deg, include_bias=False)
    T_poly = poly.fit_transform(T_lf)
    lr = LinearRegression().fit(T_poly, y)
    y_pred = lr.predict(T_poly)

    r2 = r2_score(y, y_pred)
    rmse = np.sqrt(mean_squared_error(y, y_pred))

    # Pearson 检验 y vs t（基因表达与时间的关联）
    r_pearson, p_pearson = stats.pearsonr(T_lf.ravel(), y)

    # 残差方差
    residuals = y - y_pred
    n_pts = len(y)
    p_params = best_deg + 1
    residual_var = (np.sum(residuals**2) / (n_pts - p_params - 1)) if n_pts > p_params + 1 else np.var(residuals)

    if r2 > 0.5 and rmse < 0.1 and p_pearson < 0.05:
        significant_modules.append(mod_id)

    residual_warn = '' if residual_var < 0.05 else ' [WARNING]残差方差过大，建议增加抽样量'
    print(f'  模块 {mod_id}: deg={best_deg}, R^2={r2:.4f}, RMSE={rmse:.4f}, '
          f'Pearson(y,t) r={r_pearson:.4f}, p={p_pearson:.4f}, 残差方差={residual_var:.4f}{residual_warn}')

print(f'\n显著趋势模块 (R^2>0.5, RMSE<0.1, p<0.05): {len(significant_modules)}/{optimal_k}')

# ============================================================
# 负对照实验：随机打乱时间点
# ============================================================
print('\n' + '=' * 60)
print('负对照实验：随机打乱时间点')
print('=' * 60)

r2_shuffled_all = []
N_SHUFFLE = 100
for _ in range(N_SHUFFLE):
    T_shuffled = T_lf.copy()
    np.random.shuffle(T_shuffled)
    r2_list = []
    for mod_id in range(optimal_k):
        y = module_expr[cells_lf, mod_id]
        poly = PolynomialFeatures(degree=3, include_bias=False)
        T_poly = poly.fit_transform(T_shuffled)
        lr = LinearRegression().fit(T_poly, y)
        y_pred = lr.predict(T_poly)
        r2_list.append(r2_score(y, y_pred))
    r2_shuffled_all.append(np.mean(r2_list))

r2_original_mean = np.mean([all_fitting_results[m]['degree'][3]['r2'] for m in range(optimal_k)])
r2_shuffled_threshold = np.percentile(r2_shuffled_all, 95)

print(f'  原始平均R^2: {r2_original_mean:.4f}')
print(f'  打乱后R^2的95%分位数: {r2_shuffled_threshold:.4f}')
print(f'  {"[OK] 轨迹可信" if r2_original_mean > r2_shuffled_threshold else "[FAIL] 轨迹可能不可靠"}')

# ============================================================
# 步骤6：细胞轨迹排序（选做, Left分支）
# ============================================================
print('\n' + '=' * 60)
print('步骤6：基于基因投票的细胞轨迹排序 (Left分支)')
print('=' * 60)

n_sampled = len(cells_lf)
vote_matrix = np.zeros((n_sampled, n_sampled))

for mod_id in significant_modules if significant_modules else range(optimal_k):
    y_pred = all_fitting_results[mod_id]['degree'][3]['y_pred']
    trend_r, _ = stats.pearsonr(T_lf.ravel(), y_pred)
    is_rising = trend_r > 0
    for i in range(n_sampled):
        for j in range(n_sampled):
            if is_rising:
                if y_pred[i] < y_pred[j]:
                    vote_matrix[i, j] += 1
            else:
                if y_pred[i] > y_pred[j]:
                    vote_matrix[i, j] += 1

cell_scores = vote_matrix.sum(axis=1)
sorted_order = np.argsort(-cell_scores)

# 用伪时间真值验证（仅用于验证，不参与排序过程）
true_pseudotimes = labels_df.iloc[cells_lf]['pseudotime'].values
spearman_r, spearman_p = stats.spearmanr(sorted_order, true_pseudotimes)
print(f'  排序 vs 伪时间 Spearman r={spearman_r:.4f}, p={spearman_p:.4f}')

# NMI和ARI验证 —— 基于Left分支抽样细胞
from sklearn.metrics import normalized_mutual_info_score, adjusted_rand_score

branch_order_map = {
    'Start': 0, 'Left_Mid': 1, 'Left_End': 2,
    'Right_Mid': 1, 'Right_End': 2
}
labels_df['stage'] = labels_df['branch'].map(branch_order_map)

true_stages_sampled = labels_df.iloc[cells_lf]['stage'].values.astype(int)

# 根据基因投票排序结果预测阶段（正确做法）
# sorted_order 是按投票得分从高到低排序的细胞索引
# 我们假设排序靠前的细胞更接近分化后期（End阶段），靠后的更接近早期（Start阶段）

# 方案1：基于排序位置的阶段预测（线性划分）
# 获取真实阶段的分布
stage_counts = {s: (true_stages_sampled == s).sum() for s in sorted(np.unique(true_stages_sampled))}
stage_ids = sorted(stage_counts.keys())  # [0, 1, 2]

# 根据投票排序结果预测阶段
predicted_stages = np.zeros(n_sampled, dtype=int)
# sorted_order 是按投票得分降序排列的细胞索引
# 得分高的 -> End阶段(2), 得分低的 -> Start阶段(0)
for i, cell_idx in enumerate(sorted_order):
    # 将排序位置映射到阶段
    # 位置0（得分最高）-> 阶段2（End），位置n_sampled-1（得分最低）-> 阶段0（Start）
    stage_ratio = i / (n_sampled - 1) if n_sampled > 1 else 0.5
    # 从阶段0到阶段2线性映射
    pred_stage = int(np.round(stage_ratio * (max(stage_ids) - min(stage_ids))))
    predicted_stages[cell_idx] = pred_stage

nmi = normalized_mutual_info_score(true_stages_sampled, predicted_stages)
ari = adjusted_rand_score(true_stages_sampled, predicted_stages)
print(f'  NMI = {nmi:.4f}, ARI = {ari:.4f}')
print(f'  {"[OK] 排序合理" if nmi > 0.6 and ari > 0.5 else "[WARN] 排序精度一般"}')

# ============================================================
# 可视化
# ============================================================
print('\n' + '=' * 60)
print('生成可视化图表')
print('=' * 60)

fig, axes = plt.subplots(2, 3, figsize=(18, 12))

# 图1：轮廓系数曲线
ax = axes[0, 0]
ax.plot(k_range, silhouette_scores, 'o-', color='steelblue', markersize=8)
ax.set_xlabel('cluster number k')
ax.set_ylabel('Silhouette Score')
ax.set_title('K-means Silhouette Score')
ax.grid(True, alpha=0.3)

# 图2：OLS vs Lasso 拟合对比 (Left分支)
best_mod = significant_modules[0] if significant_modules else (np.argmax(
    [all_fitting_results[m]['degree'][3]['r2'] for m in range(optimal_k)]))
ax = axes[0, 1]
y = module_expr[cells_lf, best_mod]
sort_idx = np.argsort(T_lf.ravel())
T_sorted = T_lf.ravel()[sort_idx]

y_pred_ols = all_fitting_results[best_mod]['degree'][3]['y_pred'][sort_idx]
ax.scatter(T_lf.ravel(), y, alpha=0.5, s=20, label='actual', color='gray')
ax.plot(T_sorted, y_pred_ols, '-', color='steelblue', linewidth=2, label='OLS deg=3')

y_pred_lasso = all_fitting_results[best_mod]['lasso'][3]['y_pred'][sort_idx]
lam_used = all_fitting_results[best_mod]['lasso'][3]['lambda']
ax.plot(T_sorted, y_pred_lasso, '--', color='darkorange', linewidth=2,
        label=f'Lasso lambda={lam_used}')
ax.set_xlabel('Time')
ax.set_ylabel('Expression')
ax.set_title(f'Module {best_mod} Fitting')
ax.legend()
ax.grid(True, alpha=0.3)

# 图3：lambda-CV误差曲线
ax = axes[0, 2]
lams = list(avg_cv_rmse_lasso.keys())
rmse_vals = list(avg_cv_rmse_lasso.values())
ax.semilogx(lams, rmse_vals, 'o-', color='steelblue', markersize=8)
ax.axhline(avg_cv_rmse_ols, color='red', linestyle='--',
           label=f'OLS CV-RMSE={avg_cv_rmse_ols:.4f}')
ax.set_xlabel('lambda')
ax.set_ylabel('Mean CV-RMSE')
ax.set_title('lambda - CV Error Curve')
ax.legend()
ax.grid(True, alpha=0.3)

# 图4：同阶 OLS vs Lasso R^2 对比
ax = axes[1, 0]
x_pos = np.arange(len(degrees))
width = 0.35
for rng_deg, deg in enumerate(degrees):
    ols_r2 = np.mean([all_fitting_results[m]['degree'][deg]['r2'] for m in range(optimal_k)])
    lasso_r2 = np.mean([all_fitting_results[m]['lasso'][deg]['r2'] for m in range(optimal_k)])
    ax.bar(rng_deg - width/2, ols_r2, width, label='OLS' if rng_deg == 0 else '',
           color='steelblue', alpha=0.7)
    ax.bar(rng_deg + width/2, lasso_r2, width, label='Lasso' if rng_deg == 0 else '',
           color='darkorange', alpha=0.7)
ax.set_xticks(x_pos)
ax.set_xticklabels([str(d) for d in degrees])
ax.set_xlabel('Polynomial Degree')
ax.set_ylabel('Mean R^2')
ax.set_title('OLS vs Lasso by Degree')
ax.legend()
ax.grid(True, alpha=0.3)

# 图5：负对照实验分布
ax = axes[1, 1]
ax.hist(r2_shuffled_all, bins=20, color='lightgray', edgecolor='darkgray', alpha=0.7)
ax.axvline(r2_original_mean, color='red', linestyle='--', linewidth=2,
           label=f'Original R^2={r2_original_mean:.4f}')
ax.axvline(r2_shuffled_threshold, color='blue', linestyle=':', linewidth=2,
           label=f'95%={r2_shuffled_threshold:.4f}')
ax.set_xlabel('Mean R^2')
ax.set_ylabel('Frequency')
ax.set_title(f'Negative Control (N={N_SHUFFLE})')
ax.legend()
ax.grid(True, alpha=0.3)

# 图6：轨迹排序验证 (Left分支)
ax = axes[1, 2]
true_pt = labels_df.iloc[cells_lf]['pseudotime'].values
sort_by_true = np.argsort(true_pt)
ax.scatter(np.arange(n_sampled), cell_scores[sort_by_true], alpha=0.5, s=15, color='steelblue')
ax.set_xlabel('Cells sorted by pseudotime')
ax.set_ylabel('Vote Score')
ax.set_title(f'Trajectory Validation (Spearman r={spearman_r:.4f})')
ax.grid(True, alpha=0.3)
z = np.polyfit(np.arange(n_sampled), cell_scores[sort_by_true], 1)
p_line = np.poly1d(z)
ax.plot(np.arange(n_sampled), p_line(np.arange(n_sampled)), 'r--', linewidth=1.5)

plt.tight_layout()
fig.savefig(f'{BASE_DIR}/{DATASET}/experiment3_results.png', dpi=150, bbox_inches='tight')
plt.close()
print(f'图表已保存: {BASE_DIR}/{DATASET}/experiment3_results.png')

# ============================================================
# 汇总报告
# ============================================================
print('\n' + '=' * 60)
print('Experiment 3 - Results Summary')
print('=' * 60)
print(f'\nDataset: {DATASET} (simulated, two-branch)')
print(f'Total cells: {n_cells}, HVG: {n_genes}')
print(f'Gene modules: {optimal_k}')
print(f'Sampled cells: {n_sampled} (Left: {(all_branches=="Left").sum()}, '
      f'Right: {(all_branches=="Right").sum()})')
print(f'Significant modules: {len(significant_modules)}/{optimal_k}')
print(f'\n--- Fitting Performance ---')
print(f'OLS deg=3 mean R^2: {r2_original_mean:.4f}, RMSE: {np.mean([all_fitting_results[m]["degree"][3]["rmse"] for m in range(optimal_k)]):.4f}')
print(f'Best Lasso lambda (CV): {best_lam_cv}, CV-RMSE: {avg_cv_rmse_lasso[best_lam_cv]:.4f}')
print(f'\n--- Validation ---')
print(f'Negative control: {"PASS" if r2_original_mean > r2_shuffled_threshold else "FAIL"}')
print(f'Spearman r: {spearman_r:.4f} (p={spearman_p:.4f})')
print(f'NMI: {nmi:.4f}, ARI: {ari:.4f}')
print(f'\n{"=" * 60}')
print('Experiment complete!')
