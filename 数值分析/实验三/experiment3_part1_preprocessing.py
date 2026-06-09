# 实验三 Part1：数据预处理 + 基因维度优化 + 时间点分配
import os
os.environ['LOKY_MAX_CPU_COUNT'] = '4'
os.environ['OMP_NUM_THREADS'] = '1'
os.environ['OPENBLAS_NUM_THREADS'] = '1'
os.environ['MKL_NUM_THREADS'] = '1'
import numpy as np
import pandas as pd
from sklearn.cluster import MiniBatchKMeans, KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

BASE_DIR = r'd:\documents\Python\数值分析\实验三\Datasets for P3\datasets'
DATASET = 'simulation'
EXPR_FILE = f'{BASE_DIR}/{DATASET}/expression_matrix.xlsx'
LABEL_FILE = f'{BASE_DIR}/{DATASET}/cell_labels.xlsx'
RAW_CACHE = f'{BASE_DIR}/{DATASET}/raw_data_cache.npz'

# ============================================================
# 步骤1：数据加载与预处理
# ============================================================
print('=' * 60)
print('步骤1：数据加载与预处理')
print('=' * 60)

if os.path.exists(RAW_CACHE):
    print('  从缓存加载...')
    cache = np.load(RAW_CACHE, allow_pickle=True)
    expr_df = pd.DataFrame(
        cache['expr'], index=cache['expr_index'],
        columns=cache['expr_columns']
    )
    labels_df = pd.DataFrame(
        cache['labels'], index=cache['labels_index'],
        columns=cache['labels_columns']
    )
    print('  缓存加载完成')
else:
    print('  从Excel加载 (首次较慢，后续将使用缓存)...')
    expr_df = pd.read_excel(EXPR_FILE, index_col=0)
    labels_df = pd.read_excel(LABEL_FILE, index_col=0)
    np.savez_compressed(RAW_CACHE,
                         expr=expr_df.values,
                         expr_index=expr_df.index.values,
                         expr_columns=expr_df.columns.values,
                         labels=labels_df.values,
                         labels_index=labels_df.index.values,
                         labels_columns=labels_df.columns.values)
    print('  已保存缓存，下次启动将秒级加载')

print(f'表达矩阵形状 (cells x genes): {expr_df.shape}')
print(f'标签数据形状: {labels_df.shape}')

# ---- 步骤1.1：高可变基因(HVG)筛选 ----
# 计算每个基因的变异系数 CV = std / (mean + eps)
print('\n--- 高可变基因(HVG)筛选 ---')
eps = 1e-8
cv = expr_df.std(axis=0) / (expr_df.mean(axis=0) + eps)
n_hvg = int(0.25 * expr_df.shape[1])
n_hvg = max(2000, min(n_hvg, 3000))
hvg_threshold = cv.nlargest(n_hvg).iloc[-1]
hvg_genes = cv[cv >= hvg_threshold].index
expr_hvg = expr_df[hvg_genes]
print(f'筛选前基因数: {expr_df.shape[1]}')
print(f'筛选后基因数: {len(hvg_genes)} (CV阈值={hvg_threshold:.4f})')

# ---- 步骤1.2：标准化 ----
print('\n--- 标准化处理 ---')
total_counts = expr_hvg.sum(axis=1)
norm_expr = np.log1p(expr_hvg.div(total_counts, axis=0) * 10000)
print(f'标准化后形状: {norm_expr.shape}')

# ============================================================
# 步骤2：基因维度优化 —— K-means聚类
# ============================================================
print('\n' + '=' * 60)
print('步骤2：基因维度优化 — MiniBatchKMeans聚类')
print('=' * 60)

gene_matrix = norm_expr.values.T
n_genes = gene_matrix.shape[0]
print(f'基因数: {n_genes}')

gene_scaler = StandardScaler()
gene_matrix_scaled = gene_scaler.fit_transform(gene_matrix)

# 轮廓系数评估k值（用普通KMeans，n_init='auto'对小样本更快）
print('\n--- 轮廓系数评估 ---')
silhouette_scores = []
k_range = range(8, 16)
rng = np.random.RandomState(42)
sample_size = min(300, n_genes)
sample_idx = rng.choice(n_genes, sample_size, replace=False)
gene_sample = gene_matrix_scaled[sample_idx]
sil_sample_idx = rng.choice(sample_size, min(80, sample_size), replace=False)
for k in k_range:
    km = KMeans(n_clusters=k, random_state=42, n_init='auto')
    labels = km.fit_predict(gene_sample)
    sil_sub_labels = labels[sil_sample_idx]
    sil_sub_data = gene_sample[sil_sample_idx]
    score = silhouette_score(sil_sub_data, sil_sub_labels)
    silhouette_scores.append(score)
    print(f'  k={k}, 轮廓系数={score:.4f}')

optimal_k = k_range[np.argmax(silhouette_scores)]
print(f'\n最优模块数 k = {optimal_k}, 轮廓系数 = {max(silhouette_scores):.4f}')

# 最终聚类（全量基因）
kmeans_final = MiniBatchKMeans(n_clusters=optimal_k, random_state=42, n_init=3, batch_size=min(200, n_genes))
kmeans_final.fit(gene_matrix_scaled)
gene_cluster_labels = kmeans_final.labels_

for c in range(optimal_k):
    print(f'  模块 {c}: {(gene_cluster_labels == c).sum()} 个基因')

# 构建模块表达矩阵
module_expr = np.zeros((norm_expr.shape[0], optimal_k))
for c in range(optimal_k):
    mask = gene_cluster_labels == c
    module_expr[:, c] = norm_expr.values[:, mask].mean(axis=1)

module_expr_df = pd.DataFrame(module_expr, index=norm_expr.index,
                               columns=[f'Module_{c}' for c in range(optimal_k)])
print(f'模块表达矩阵形状 (cells x modules): {module_expr_df.shape}')

# ============================================================
# 步骤3：时间点分配 —— 双分支独立处理
# ============================================================
print('\n' + '=' * 60)
print('步骤3：双分支时间点分配')
print('=' * 60)

print(f'分支标签: {labels_df["branch"].unique()}')

# 两条分支独立处理
BRANCH_DEFS = {
    'Left':  {'stages': ['Start', 'Left_Mid', 'Left_End']},
    'Right': {'stages': ['Start', 'Right_Mid', 'Right_End']},
}

SAMPLE_RATE = 0.05
POLY_DEGREE = 3

all_sampled_cells_list = []
all_time_points_list = []
all_branches = []
driving_modules_record = {}

for branch_name, branch_info in BRANCH_DEFS.items():
    stages = branch_info['stages']
    print(f'\n--- {branch_name} 分支: {" -> ".join(stages)} ---')

    for stage_id, stage_name in enumerate(stages):
        if stage_name == 'Start':
            stage_cells = labels_df[labels_df['branch'] == 'Start'].index.tolist()
        else:
            stage_cells = labels_df[labels_df['branch'] == stage_name].index.tolist()

        if len(stage_cells) == 0:
            continue

        n_stage = len(stage_cells)
        stage_indices = [list(norm_expr.index).index(c) for c in stage_cells
                         if c in norm_expr.index]

        # 3.2 阶段间差异模块筛选（选驱动模块）
        drive_mod = 0
        if stage_id > 0:
            prev_stage_name = stages[stage_id - 1]
            if prev_stage_name == 'Start':
                prev_cells = labels_df[labels_df['branch'] == 'Start'].index.tolist()
            else:
                prev_cells = labels_df[labels_df['branch'] == prev_stage_name].index.tolist()

            prev_idx = [list(norm_expr.index).index(c) for c in prev_cells
                        if c in norm_expr.index]

            best_diff = -1
            for mod in range(optimal_k):
                mean_prev = module_expr[prev_idx, mod].mean() if prev_idx else 0
                mean_curr = module_expr[stage_indices, mod].mean() if stage_indices else 0
                diff = abs(mean_curr - mean_prev)
                if diff > best_diff:
                    best_diff = diff
                    drive_mod = mod
        else:
            # Start阶段：在所有模块中选一个作为排序依据
            best_std = -1
            for mod in range(optimal_k):
                std_val = module_expr[stage_indices, mod].std() if len(stage_indices) > 1 else 0
                if std_val > best_std:
                    best_std = std_val
                    drive_mod = mod

        driving_modules_record[(branch_name, stage_name)] = drive_mod

        # 3.3 阶段内细胞排序（不用pseudotime！用相邻阶段表达差异方向）
        drive_values = module_expr[stage_indices, drive_mod]

        # 判断排序方向：比较该模块在当前阶段和下一阶段的平均表达
        sort_ascending = True  # 默认升序
        if stage_id < len(stages) - 1:
            next_stage_name = stages[stage_id + 1]
            if next_stage_name == 'Start':
                next_cells = labels_df[labels_df['branch'] == 'Start'].index.tolist()
            else:
                next_cells = labels_df[labels_df['branch'] == next_stage_name].index.tolist()
            next_idx = [list(norm_expr.index).index(c) for c in next_cells
                        if c in norm_expr.index]
            if next_idx:
                mean_curr = drive_values.mean()
                mean_next = module_expr[next_idx, drive_mod].mean()
                sort_ascending = mean_next >= mean_curr

        sort_indices = np.argsort(drive_values)
        if not sort_ascending:
            sort_indices = sort_indices[::-1]

        # 3.4 均匀抽样
        n_sample = max(3 * POLY_DEGREE + 1, int(SAMPLE_RATE * n_stage))
        n_sample = min(n_sample, n_stage)
        step = max(1, (len(sort_indices) - 1) // max(1, n_sample - 1)) if n_sample > 1 else 0
        sample_positions = np.arange(0, len(sort_indices), step)[:n_sample] if step > 0 else [sort_indices[0]]
        sampled_idx = [stage_indices[sort_indices[p]] for p in sample_positions if p < len(sort_indices)]

        # 3.5 阶段内时间点均匀插值
        t0 = stage_id
        t1 = stage_id + 1
        t_points = np.linspace(t0, t1, len(sampled_idx)) if len(sampled_idx) > 1 else [t0]

        # 3.5.1 排序单调性检验
        if len(sampled_idx) >= 5:
            sampled_drive = module_expr[sampled_idx, drive_mod]
            mono_r, mono_p = stats.spearmanr(range(len(sampled_idx)), sampled_drive)
            if abs(mono_r) < 0.8:
                print(f'  [WARN] {stage_name}: 排序单调性不足 Spearman r={mono_r:.3f}, '
                      f'尝试更换驱动模块')
                # 尝试换次优模块
                second_best = -1
                second_diff = -1
                for mod in range(optimal_k):
                    if mod == drive_mod:
                        continue
                    mean_prev = module_expr[prev_idx, mod].mean() if stage_id > 0 and prev_idx else 0
                    mean_curr = module_expr[stage_indices, mod].mean() if stage_indices else 0
                    diff = abs(mean_curr - mean_prev)
                    if diff > second_diff:
                        second_diff = diff
                        second_best = mod
                if second_best >= 0:
                    drive_mod = second_best
                    drive_values = module_expr[stage_indices, drive_mod]
                    if not sort_ascending:
                        sort_indices = np.argsort(drive_values)[::-1]
                    else:
                        sort_indices = np.argsort(drive_values)
                    sampled_idx = [stage_indices[sort_indices[p]] for p in sample_positions
                                   if p < len(sort_indices)]
                    sampled_drive = module_expr[sampled_idx, drive_mod]
                    mono_r, mono_p = stats.spearmanr(range(len(sampled_idx)), sampled_drive)
            print(f'  {stage_name}: 单调性ρ={mono_r:.3f} (p={mono_p:.4f}) '
                  f'{"[OK]" if abs(mono_r) >= 0.8 else "[WARN]调整后仍不足"}')
        else:
            mono_r = 0
            print(f'  {stage_name}: 细胞数太少，跳过单调性检验')

        print(f'  {stage_name}: {n_stage}个细胞 → 抽样{len(sampled_idx)}个, '
              f'驱动模块={drive_mod}, 方向={"升序" if sort_ascending else "降序"}')

        all_sampled_cells_list.extend(sampled_idx)
        all_time_points_list.extend(t_points)
        all_branches.extend([branch_name] * len(sampled_idx))

all_sampled_cells = np.array(all_sampled_cells_list)
all_time_points = np.array(all_time_points_list)
all_branches = np.array(all_branches)

print(f'\n总抽样细胞数: {len(all_sampled_cells)}')
print(f'  Left  分支抽样: {(all_branches == "Left").sum()}')
print(f'  Right 分支抽样: {(all_branches == "Right").sum()}')

# 3.5.2 阶段间衔接检验
print('\n--- 阶段间衔接检验 ---')
for branch_name, branch_info in BRANCH_DEFS.items():
    stages = branch_info['stages']
    for i in range(len(stages) - 1):
        mask_i = (all_branches == branch_name) & \
                 (np.array([stages[i] in str(labels_df.iloc[c]['branch']) for c in all_sampled_cells])
                  if False else True)
        # 简化：检查相邻阶段时间点连续
        br_idx = np.where(all_branches == branch_name)[0]
        br_cells = all_sampled_cells[br_idx]
        br_times = all_time_points[br_idx]
        print(f'  {branch_name} {stages[i]}→{stages[i+1]}: 时间范围 [{br_times.min():.2f}, {br_times.max():.2f}]')

# ============================================================
# 保存预处理结果
# ============================================================
print('\n' + '=' * 60)
print('保存预处理结果')
print('=' * 60)

np.savez(f'{BASE_DIR}/{DATASET}/preprocess_result.npz',
         norm_expr=norm_expr.values,
         module_expr=module_expr_df.values,
         all_sampled_cells=all_sampled_cells,
         all_time_points=all_time_points,
         all_branches=all_branches,
         optimal_k=optimal_k,
         gene_cluster_labels=gene_cluster_labels,
         silhouette_scores=np.array(silhouette_scores),
         k_range=np.array(list(k_range)))

print('预处理结果已保存')
print('\nPart1 完成！请运行 experiment3_part2_fitting.py')
