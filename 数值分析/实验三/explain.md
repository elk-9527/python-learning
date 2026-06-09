# 实验三：单细胞基因表达最小二乘拟合及细胞分化轨迹解析 —— 数学原理详解

---

## 目录

1. [高可变基因筛选（HVG Selection）](#1-高可变基因筛选)
2. [表达矩阵标准化（Normalization）](#2-表达矩阵标准化)
3. [K-means 聚类与基因模块构建](#3-k-means-聚类与基因模块构建)
4. [轮廓系数与最优聚类数选择](#4-轮廓系数与最优聚类数选择)
5. [时间点分配策略](#5-时间点分配策略)
6. [普通最小二乘多项式拟合（OLS）](#6-普通最小二乘多项式拟合)
7. [Lasso 正则化最小二乘拟合](#7-lasso-正则化最小二乘拟合)
8. [K 折交叉验证与 λ 选择](#8-k-折交叉验证与-λ-选择)
9. [拟合优度与误差分析](#9-拟合优度与误差分析)
10. [假设检验](#10-假设检验)
11. [负对照实验：时间点随机打乱](#11-负对照实验时间点随机打乱)
12. [基于投票的细胞轨迹排序](#12-基于投票的细胞轨迹排序)
13. [NMI 与 ARI 轨迹验证](#13-nmi-与-ari-轨迹验证)
14. [数值实现细节](#14-数值实现细节)

---

## 1. 高可变基因筛选

### 1.1 问题背景

单细胞 RNA-seq 表达矩阵通常包含数万个基因，但其中大量基因为低表达或无差异表达的"噪声基因"。高可变基因（Highly Variable Genes, HVG）筛选的目标是保留表达变异系数（Coefficient of Variation, CV）最大的前 20%–30% 基因，从而在保留生物学信息的前提下大幅降低计算维度。

### 1.2 变异系数的定义

对于基因 $i$（$i = 1, 2, \dots, N_{genes}$），其在所有细胞中的表达向量为：

$$
\mathbf{g}_i = [x_{i1}, x_{i2}, \dots, x_{im}]^T
$$

其中 $m$ 为细胞总数。

变异系数（CV）定义为标准差与均值的比值：

$$
CV_i = \frac{\sigma_i}{\mu_i + \varepsilon}
$$

其中：

- $\displaystyle \mu_i = \frac{1}{m} \sum_{j=1}^{m} x_{ij}$ — 基因 $i$ 在所有细胞上的表达均值
- $\displaystyle \sigma_i = \sqrt{\frac{1}{m-1} \sum_{j=1}^{m} (x_{ij} - \mu_i)^2}$ — 基因 $i$ 表达量的标准差（或在代码中使用的总体标准差 $\sqrt{\frac{1}{m} \sum (x_{ij} - \mu_i)^2}$）
- $\varepsilon = 10^{-8}$ — 极小正则化常数，防止 $\mu_i = 0$ 时除零错误

### 1.3 筛选策略

对所有基因计算 $CV_i$，按降序排列，取前 $n_{HVG}$ 个基因：

$$
n_{HVG} = \text{clamp}\left(\lfloor 0.25 \times N_{genes} \rfloor,\; 2000,\; 3000\right)
$$

即保留 25% 的基因，但控制在 2000–3000 之间。设阈值 $\tau_{CV}$ 为第 $n_{HVG}$ 大的 $CV$ 值，则筛选后的基因集合为：

$$
\mathcal{G}_{HVG} = \{ g_i \mid CV_i \geq \tau_{CV} \}
$$

### 1.4 代码实现

```python
cv = expr_df.std(axis=0) / (expr_df.mean(axis=0) + eps)
n_hvg = int(0.25 * expr_df.shape[1])
n_hvg = max(2000, min(n_hvg, 3000))
hvg_threshold = cv.nlargest(n_hvg).iloc[-1]
hvg_genes = cv[cv >= hvg_threshold].index
expr_hvg = expr_df[hvg_genes]
```

---

## 2. 表达矩阵标准化

### 2.1 问题背景

不同细胞的测序深度（总 reads 数）差异巨大，直接比较原始表达量会产生系统性偏差。标准化（Normalization）的目的是消除这种测序深度差异，使不同细胞之间的基因表达量具有可比性。

### 2.2 数学公式

采用 Seurat 标准方法——对数归一化（Log-Normalization）：

$$
X_{ij}^{\text{norm}} = \ln\left(1 + \frac{X_{ij}}{\displaystyle \sum_{k} X_{kj}} \times S\right)
$$

其中：

- $X_{ij}$ — 基因 $i$ 在细胞 $j$ 中的原始表达量（原始 counts 或 TPM）
- $\sum_k X_{kj}$ — 细胞 $j$ 的总表达量（library size）
- $S = 10000$ — 缩放因子（scale factor），将表达量统一缩放到"每 10000 reads"的尺度
- $\ln(1 + \cdot)$ — $\ln(1+x)$ 变换（即 $\log 1p$），起到以下作用：
  1. **压缩极端值**：对数变换将高表达基因的值压缩，减少少数极高表达基因对分析的过度影响
  2. **稳定方差**：使不同表达水平的基因具有更均匀的方差
  3. **近似正态化**：使表达分布更接近正态分布，便于后续统计检验

### 2.3 矩阵形式

设原始表达矩阵为 $\mathbf{X} \in \mathbb{R}^{m \times n_{HVG}}$，标准化矩阵 $\mathbf{X}^{\text{norm}}$ 的每个元素为：

$$
\mathbf{X}^{\text{norm}} = \ln\left(\mathbf{1} + \mathbf{D}^{-1} \mathbf{X} \times S\right)
$$

其中 $\mathbf{D} = \operatorname{diag}(s_1, s_2, \dots, s_m)$ 为对角矩阵，$s_j = \sum_k X_{kj}$ 为每行的总 reads 数。

### 2.4 代码实现

```python
total_counts = expr_hvg.sum(axis=1)
norm_expr = np.log1p(expr_hvg.div(total_counts, axis=0) * 10000)
```

---

## 3. K-means 聚类与基因模块构建

### 3.1 问题背景

即使经过 HVG 筛选，基因维度仍有 2000–3000 维。对每个基因单独进行最小二乘拟合计算量巨大，且单个基因的噪音较大。K-means 聚类将表达模式相似的基因归入同一模块，用模块中心向量（模块内所有基因表达的均值）替代单基因进行后续分析，实现维度压缩。

### 3.2 输入数据的构造

将标准化表达矩阵转置，使每行对应一个基因、每列对应一个细胞：

$$
\mathbf{G} = (\mathbf{X}^{\text{norm}})^T \in \mathbb{R}^{n_{HVG} \times m}
$$

其中第 $i$ 行 $\mathbf{g}_i = [x_{i1}^{\text{norm}}, x_{i2}^{\text{norm}}, \dots, x_{im}^{\text{norm}}]$ 为基因 $i$ 在所有 $m$ 个细胞上的标准化表达向量。

为进一步消除不同基因表达量级的差异，对基因向量进行 Z-score 标准化：

$$
\tilde{g}_{ij} = \frac{g_{ij} - \bar{g}_i}{\sigma_{g_i}}
$$

其中 $\bar{g}_i$ 和 $\sigma_{g_i}$ 分别为基因 $i$ 的均值和标准差。

### 3.3 K-means 目标函数

K-means 聚类将 $n_{HVG}$ 个基因划分为 $k$ 个互不相交的模块 $C_1, C_2, \dots, C_k$，使得模块内平方和误差（Within-Cluster Sum of Squares, WCSS）最小：

$$
SSE = \sum_{c=1}^{k} \sum_{\mathbf{g}_i \in C_c} \| \mathbf{g}_i - \boldsymbol{\mu}_c \|^2
$$

其中：

- $C_c$ — 第 $c$ 个基因模块（簇）
- $\mathbf{g}_i$ — 基因 $i$ 的标准化表达向量（$1 \times m$）
- $\boldsymbol{\mu}_c$ — 第 $c$ 个模块的中心向量（质心），定义为模块内所有基因向量的均值：

$$
\boldsymbol{\mu}_c = \frac{1}{|C_c|} \sum_{\mathbf{g}_i \in C_c} \mathbf{g}_i
$$

- $\|\cdot\|$ — 欧氏距离（$L_2$ 范数）：$\|\mathbf{a} - \mathbf{b}\| = \sqrt{\sum_j (a_j - b_j)^2}$

### 3.4 迭代算法流程

K-means 通过 Lloyd 算法迭代求解：

1. **初始化**：随机选取 $k$ 个基因作为初始质心（或用 K-means++ 初始化）
2. **分配步骤**：将每个基因 $\mathbf{g}_i$ 分配给距离最近的质心：

   $$
   c^{(i)} = \arg\min_c \|\mathbf{g}_i - \boldsymbol{\mu}_c\|^2
   $$

3. **更新步骤**：重新计算每个模块的质心：

   $$
   \boldsymbol{\mu}_c = \frac{1}{|C_c|} \sum_{\mathbf{g}_i \in C_c} \mathbf{g}_i
   $$

4. 重复步骤 2–3 直到质心变化小于收敛阈值或达到最大迭代次数。

### 3.5 MiniBatchKMeans 加速

代码中使用 `MiniBatchKMeans` 替代标准 K-means，其本质是用小批量随机梯度下降近似标准 K-means：

- 每次迭代只使用一个随机小批量（batch）的样本更新质心
- 质心更新公式为指数移动平均：

  $$
  \boldsymbol{\mu}_c^{(t+1)} = \boldsymbol{\mu}_c^{(t)} + \eta_t \cdot (\bar{\mathbf{g}}_c^{(batch)} - \boldsymbol{\mu}_c^{(t)})
  $$

  其中 $\eta_t = \frac{1}{n_c^{(t)}}$ 为学习率（$n_c^{(t)}$ 为截至当前已分配给该簇的累计样本数），$\bar{\mathbf{g}}_c^{(batch)}$ 为当前 batch 中属于簇 $c$ 的样本均值。

- 优势：时间复杂度从 $O(n_{HVG} \cdot k \cdot m \cdot T)$ 降至 $O(batch\_size \cdot k \cdot m \cdot T)$，适合大数据集。

### 3.6 模块表达矩阵的构建

聚类完成后，对每个模块 $c$，在所有 $m$ 个细胞上计算模块中心表达值：

$$
E_{jc} = \frac{1}{|C_c|} \sum_{g_i \in C_c} X_{ij}^{\text{norm}},\quad j = 1, 2, \dots, m
$$

得到模块表达矩阵 $\mathbf{E} \in \mathbb{R}^{m \times k}$，维度从 $n_{HVG}$（2000–3000）压缩到 $k$（8–15）。

### 3.7 代码实现

```python
scaler = StandardScaler()
gene_matrix_scaled = scaler.fit_transform(gene_matrix)  # Z-score normalization

kmeans_final = MiniBatchKMeans(n_clusters=optimal_k, random_state=42, ...)
kmeans_final.fit(gene_matrix_scaled)
gene_cluster_labels = kmeans_final.labels_

# Build module expression matrix
module_expr = np.zeros((n_cells, optimal_k))
for c in range(optimal_k):
    mask = gene_cluster_labels == c
    module_expr[:, c] = norm_expr.values[:, mask].mean(axis=1)
```

---

## 4. 轮廓系数与最优聚类数选择

### 4.1 轮廓系数定义

轮廓系数（Silhouette Coefficient）用于评估聚类质量，同时衡量簇内紧密度和簇间分离度。对每个基因 $i$，其轮廓系数为：

$$
s(i) = \frac{b(i) - a(i)}{\max\{ a(i), b(i) \}}
$$

其中：

- **$a(i)$** — 基因 $i$ 到同模块内其他基因的平均距离（簇内紧密度）：

  $$
  a(i) = \frac{1}{|C_{c(i)}| - 1} \sum_{\substack{i' \in C_{c(i)} \\ i' \neq i}} \|\mathbf{g}_i - \mathbf{g}_{i'}\|
  $$

- **$b(i)$** — 基因 $i$ 到最近异模块中所有基因的平均距离（簇间分离度）：

  $$
  b(i) = \min_{c \neq c(i)} \frac{1}{|C_c|} \sum_{i' \in C_c} \|\mathbf{g}_i - \mathbf{g}_{i'}\|
  $$

- **范围**：$s(i) \in [-1, 1]$
  - $s(i) \to 1$：基因 $i$ 被很好地聚类（$a(i) \ll b(i)$）
  - $s(i) \to 0$：基因 $i$ 处于两个簇的边界
  - $s(i) \to -1$：基因 $i$ 可能被错误分类（$a(i) > b(i)$）

### 4.2 平均轮廓系数

对所有基因取平均得到整体聚类质量指标：

$$
\bar{s} = \frac{1}{n_{HVG}} \sum_{i=1}^{n_{HVG}} s(i)
$$

### 4.3 最优 $k$ 的选择

在候选范围 $k \in \{8, 9, \dots, 15\}$ 内，选取使 $\bar{s}$ 最大的 $k$：

$$
k^* = \arg\max_{k \in \{8,\dots,15\}} \bar{s}(k)
$$

### 4.4 计算加速策略

由于基因数量庞大（2000+），计算完整的轮廓系数代价过高。代码采用双重采样加速：

1. **第一次采样**：从全部基因中随机抽取 300 个基因进行聚类
2. **第二次采样**：从 300 个基因中再随机抽取 80 个基因计算轮廓系数

这样将复杂度从 $O(n_{HVG}^2)$ 降至 $O(80^2 \cdot k)$，且保持评估的相对准确性。

### 4.5 代码实现

```python
sample_idx = rng.choice(n_genes, min(300, n_genes), replace=False)
gene_sample = gene_matrix_scaled[sample_idx]
sil_sample_idx = rng.choice(len(gene_sample), min(80, len(gene_sample)), replace=False)

for k in k_range:
    km = KMeans(n_clusters=k, random_state=42, n_init='auto')
    labels = km.fit_predict(gene_sample)
    score = silhouette_score(gene_sample[sil_sample_idx], labels[sil_sample_idx])
    silhouette_scores.append(score)
```

---

## 5. 时间点分配策略

### 5.1 全局时间轴构建

为每个已知生物学阶段分配一个连续的时间区间。有两种方式：

#### 5.1.1 固定间隔设定

设共有 $S$ 个阶段，每阶段时间长度为 1：

$$
\Delta t_i = 1,\quad t_i^{\text{start}} = i,\quad t_i^{\text{end}} = i + 1,\quad i = 0, 1, \dots, S-1
$$

以本实验为例（Start → Left_Mid → Left_End），对应时间区间为 $[0,1], [1,2], [2,3]$。

#### 5.1.2 动态间隔设定（备选方案）

区间长度正比于该阶段细胞数：

$$
\Delta t_i = \frac{N_i}{\sum_{j} N_j} \times T_{\text{total}}
$$

其中 $N_i$ 为阶段 $i$ 的细胞数，$T_{\text{total}}$ 为预设总时间。每个阶段的起始和结束时间通过累积计算：

$$
t_i^{\text{start}} = \sum_{j=0}^{i-1} \Delta t_j,\quad t_i^{\text{end}} = t_i^{\text{start}} + \Delta t_i
$$

### 5.2 阶段内排序驱动模块筛选

对于每两个相邻阶段（阶段 $i$ 和阶段 $i+1$），寻找表达差异最大的基因模块作为"排序驱动模块"。

#### 5.2.1 模块差异计算

对于模块 $c$，计算其在两个阶段的平均表达差异：

$$
\Delta E_c(i, i+1) = \left| \bar{E}_c^{(i+1)} - \bar{E}_c^{(i)} \right|
$$

其中 $\bar{E}_c^{(i)} = \frac{1}{|S_i|} \sum_{j \in S_i} E_{jc}$ 为模块 $c$ 在阶段 $i$ 所有细胞上的平均表达值，$S_i$ 为阶段 $i$ 的细胞索引集合。

#### 5.2.2 驱动模块选择

选择差异最大的模块：

$$
c^*_{\text{drive}}(i) = \arg\max_c \Delta E_c(i, i+1)
$$

对于第一个阶段（Start），由于没有前一阶段可用于对比，选择表达方差最大的模块：

$$
c^*_{\text{drive}}(0) = \arg\max_c \operatorname{Var}(E_{jc}),\quad j \in S_0
$$

#### 5.2.3 排序方向判断

比较驱动模块在当前阶段与下一阶段的平均表达，确定排序方向：

- 若 $\bar{E}_{c^*}^{(i+1)} \geq \bar{E}_{c^*}^{(i)}$，则模块表达随分化**上升**，阶段内按表达量**升序**排列
- 否则，按**降序**排列

这一判断的逻辑是：若下一阶段该模块表达更高，则阶段内发育越成熟的细胞应具有越高的模块表达。

### 5.3 阶段内细胞排序与抽样

#### 5.3.1 排序

对阶段 $i$ 内的每个细胞 $j$，计算其在驱动模块上的中心表达值：

$$
v_j = E_{j, c^*_{\text{drive}}(i)},\quad j \in S_i
$$

按排序方向对 $\{v_j\}$ 进行排序，得到阶段内的细胞顺序。

#### 5.3.2 抽样量确定

抽样量需满足两个约束条件：

$$
n_s \geq \max\left(3p + 1,\; 0.05 \times N_i\right)
$$

- $3p + 1$（$p$ 为多项式阶数）：确保参数估计的自由度——$p$ 次多项式有 $p+1$ 个参数，最少需要 $p+1$ 个数据点，$3p+1$ 提供了充足冗余
- $0.05 N_i$：确保抽样具有代表性，覆盖至少 5% 的细胞
- 最终 $n_s = \min(n_s, N_i)$，不能超过阶段细胞总数

#### 5.3.3 均匀抽样

在排序后的细胞序列中，按等间距抽取 $n_s$ 个细胞。设排序后的细胞索引序列为 $\pi_1, \pi_2, \dots, \pi_{N_i}$（$\pi_k$ 为排序后第 $k$ 个细胞在原始矩阵中的索引），采样位置为：

$$
p_q = \lfloor (q-1) \cdot \text{step} \rfloor,\quad q = 1, 2, \dots, n_s
$$

其中 $\text{step} = \max\left(1, \frac{N_i - 1}{n_s - 1}\right)$（当 $n_s > 1$ 时）。

### 5.4 阶段内时间点均匀插值

对阶段 $i$ 内抽样的 $n_s$ 个细胞（已排序），使用线性插值分配连续时间点：

$$
t_{ij} = t_i^{\text{start}} + \frac{j-1}{n_s - 1} \times (t_i^{\text{end}} - t_i^{\text{start}}),\quad j = 1, 2, \dots, n_s
$$

其中 $j$ 为细胞在阶段内的排序序号（$j=1$ 对应最早发育状态的细胞，$j=n_s$ 对应最晚发育状态的细胞）。

### 5.5 排序单调性检验

为验证阶段内排序是否合理，计算排序序号与驱动模块表达值的 Spearman 秩相关系数：

$$
\rho = \frac{\operatorname{cov}(R_X, R_Y)}{\sigma_{R_X} \sigma_{R_Y}}
$$

其中 $R_X = [1, 2, \dots, n_s]$ 为排序序号，$R_Y$ 为驱动模块表达值的秩。若 $|\rho| < 0.8$，说明排序单调性不足，尝试更换为次优差异模块重新排序。

### 5.6 双分支独立处理

对于双分支分化数据（如 Left 和 Right 分支），每个分支独立进行时间点分配。起始阶段（Start）的细胞同时出现在两个分支中，但后续阶段各自独立处理。这保证了每个分支内部的时间点分配不受另一分支的影响。

### 5.7 代码实现

```python
for branch_name, branch_info in BRANCH_DEFS.items():
    stages = branch_info['stages']
    for stage_id, stage_name in enumerate(stages):
        # ... 获取阶段细胞 ...
        
        # 选择驱动模块（阶段间差异最大）
        if stage_id > 0:
            for mod in range(optimal_k):
                diff = abs(mean_curr - mean_prev)
                if diff > best_diff:
                    drive_mod = mod
        
        # 判断排序方向
        sort_ascending = mean_next >= mean_curr
        
        # 均匀抽样
        n_sample = max(3 * POLY_DEGREE + 1, int(SAMPLE_RATE * n_stage))
        step = max(1, (len(sort_indices) - 1) // max(1, n_sample - 1))
        
        # 时间点插值
        t_points = np.linspace(t0, t1, len(sampled_idx))
```

---

## 6. 普通最小二乘多项式拟合

### 6.1 问题建模

对每个基因模块 $c$，在抽样细胞上的表达量 $\mathbf{y} = [y_1, y_2, \dots, y_{n_s}]^T$ 与对应的时间点 $\mathbf{t} = [t_1, t_2, \dots, t_{n_s}]^T$ 之间存在函数关系，用 $p$ 次多项式近似：

$$
\hat{y}(t) = a_0 + a_1 t + a_2 t^2 + \cdots + a_p t^p = \sum_{m=0}^{p} a_m t^m
$$

其中 $\mathbf{a} = [a_0, a_1, \dots, a_p]^T$ 为待拟合参数。

### 6.2 设计矩阵构造

将 $n_s$ 个数据点代入多项式形式，构造设计矩阵（Design Matrix）$\mathbf{T} \in \mathbb{R}^{n_s \times (p+1)}$：

$$
\mathbf{T} = \begin{bmatrix}
1 & t_1 & t_1^2 & \cdots & t_1^p \\
1 & t_2 & t_2^2 & \cdots & t_2^p \\
\vdots & \vdots & \vdots & \ddots & \vdots \\
1 & t_{n_s} & t_{n_s}^2 & \cdots & t_{n_s}^p
\end{bmatrix}
$$

则拟合值向量 $\hat{\mathbf{y}}$ 可表示为：

$$
\hat{\mathbf{y}} = \mathbf{T} \mathbf{a}
$$

### 6.3 残差平方和

定义残差向量 $\mathbf{e} = \mathbf{y} - \hat{\mathbf{y}} = \mathbf{y} - \mathbf{T}\mathbf{a}$，残差平方和（Residual Sum of Squares, RSS）为：

$$
RSS(\mathbf{a}) = \|\mathbf{e}\|^2 = \|\mathbf{y} - \mathbf{T}\mathbf{a}\|^2 = \sum_{j=1}^{n_s} (y_j - \hat{y}_j)^2
$$

### 6.4 正规方程与解析解

目标是最小化 $RSS(\mathbf{a})$。对 $\mathbf{a}$ 求梯度并令其为零：

$$
\nabla_{\mathbf{a}} RSS = \nabla_{\mathbf{a}} \left[ (\mathbf{y} - \mathbf{T}\mathbf{a})^T (\mathbf{y} - \mathbf{T}\mathbf{a}) \right]
$$

展开：

$$
RSS = \mathbf{y}^T\mathbf{y} - 2\mathbf{y}^T\mathbf{T}\mathbf{a} + \mathbf{a}^T\mathbf{T}^T\mathbf{T}\mathbf{a}
$$

求导：

$$
\frac{\partial RSS}{\partial \mathbf{a}} = -2\mathbf{T}^T\mathbf{y} + 2\mathbf{T}^T\mathbf{T}\mathbf{a} = 0
$$

得到正规方程（Normal Equations）：

$$
\mathbf{T}^T\mathbf{T}\mathbf{a} = \mathbf{T}^T\mathbf{y}
$$

若 $\mathbf{T}^T\mathbf{T}$ 可逆（$n_s \geq p+1$ 且 $\mathbf{T}$ 列满秩时成立），则最小二乘解为：

$$
\boxed{\mathbf{a}^* = (\mathbf{T}^T\mathbf{T})^{-1}\mathbf{T}^T\mathbf{y}}
$$

其中 $(\mathbf{T}^T\mathbf{T})^{-1}\mathbf{T}^T$ 即为 $\mathbf{T}$ 的 Moore-Penrose 伪逆 $\mathbf{T}^+$。

### 6.5 数值求解方法

在实际实现中（如 scikit-learn 的 `LinearRegression`），不直接计算伪逆，而是通过以下方式之一求解：

1. **QR 分解**：$\mathbf{T} = \mathbf{Q}\mathbf{R}$，则 $\mathbf{a}^* = \mathbf{R}^{-1}\mathbf{Q}^T\mathbf{y}$，数值更稳定
2. **SVD 分解**：$\mathbf{T} = \mathbf{U}\boldsymbol{\Sigma}\mathbf{V}^T$，则 $\mathbf{a}^* = \mathbf{V}\boldsymbol{\Sigma}^{-1}\mathbf{U}^T\mathbf{y}$

代码中使用 `PolynomialFeatures(include_bias=False)` + `LinearRegression(fit_intercept=True)`，设计矩阵不含全 1 列，由 `fit_intercept=True` 自动添加截距项，避免重复。

### 6.6 多阶拟合与最佳阶数

对每个模块分别尝试 $p \in \{1, 2, 3\}$（一次、二次、三次多项式），选择 $R^2$ 最高的阶数作为该模块的最佳拟合阶数：

$$
p^*_c = \arg\max_{p \in \{1,2,3\}} R^2_c(p)
$$

这一策略允许不同模块使用不同的多项式复杂度——有些基因模块的表达变化简单（适合一次拟合），有些则呈现非单调趋势（需要三次拟合）。

### 6.7 代码实现

```python
for deg in degrees:
    poly = PolynomialFeatures(degree=deg, include_bias=False)
    T_poly = poly.fit_transform(T_br)
    lr = LinearRegression()
    lr.fit(T_poly, y)
    y_pred = lr.predict(T_poly)
```

---

## 7. Lasso 正则化最小二乘拟合

### 7.1 过拟合问题

当多项式阶数 $p$ 较高而数据量 $n_s$ 有限时，普通最小二乘容易出现过拟合——拟合曲线在数据点之间剧烈振荡，虽然 $R^2$ 很高但对新数据的预测能力很差。

### 7.2 Lasso 正则化

Lasso（Least Absolute Shrinkage and Selection Operator）在 RSS 基础上添加 $L_1$ 正则化项，惩罚参数绝对值之和：

$$
\boxed{\min_{\mathbf{a}} \left\{ \sum_{j=1}^{n_s} \left( y_j - \sum_{m=0}^{p} a_m t_j^m \right)^2 + \lambda \sum_{m=1}^{p} |a_m| \right\}}
$$

其中：

- $\lambda \geq 0$ 为正则化参数（超参数）
- $\sum_{m=1}^{p} |a_m|$ 为 $L_1$ 惩罚项（注意通常不惩罚截距 $a_0$）
- 代码中 scikit-learn 的 `Lasso` 默认不惩罚截距（`fit_intercept=True`）

### 7.3 $L_1$ 正则化的几何意义

在参数空间中，$L_1$ 约束区域为菱形（二维时为 diamond），其顶点位于坐标轴上。当 RSS 等高线首次与菱形接触时，交点往往在坐标轴上，导致某些 $a_m = 0$——这就是 Lasso 的**稀疏性**（Sparsity）特性。这种自动特征选择使 Lasso 天然地抑制高阶项的过拟合倾向。

### 7.4 $L_1$ vs $L_2$（Ridge）

对比 Ridge 回归（$L_2$ 正则化）：

$$
\min_{\mathbf{a}} \left\{ RSS + \lambda \sum_{m=1}^{p} a_m^2 \right\}
$$

- **Ridge**：$L_2$ 约束区域为球体，参数趋向于缩小但不为零，无稀疏性
- **Lasso**：$L_1$ 约束区域为菱形，可将不重要参数压缩至零，自动特征选择
- 本实验选择 Lasso 而非 Ridge，因为 Lasso 能自动识别并剔除不必要的高阶项（如 $t^3$ 系数为零时，拟合退化为二次），在基因表达拟合场景下更具可解释性

### 7.5 $\lambda$ 的影响

- $\lambda = 0$：Lasso 退化为普通最小二乘（OLS）
- $\lambda \to \infty$：所有权重趋近于零（除截距外），拟合曲线退化为常数（均值）
- 适当的 $\lambda$：在拟合精度与模型复杂度之间取得平衡

### 7.6 数值求解：坐标下降法

scikit-learn 的 `Lasso` 使用坐标下降法（Coordinate Descent）求解。对每个参数 $a_m$，在其他参数固定时求一维最优解，通过软阈值（Soft Thresholding）更新：

$$
a_m^{(new)} = \operatorname{soft}\left( a_m^{OLS},\; \frac{\lambda}{2} \right)
$$

其中软阈值函数为：

$$
\operatorname{soft}(z, \gamma) = \operatorname{sign}(z) \cdot \max(|z| - \gamma, 0)
$$

坐标下降在 $L_1$ 正则化问题上具有闭式更新且收敛速度快的特点。

### 7.7 代码实现

```python
for lam in lasso_lambdas:
    lasso = Lasso(alpha=lam, max_iter=10000, random_state=42)
    lasso.fit(T_poly, y)
    y_pred_l = lasso.predict(T_poly)
```

---

## 8. K 折交叉验证与 λ 选择

### 8.1 为什么需要交叉验证

在训练集上直接最小化 RSS 选择 $\lambda$ 会导致 $\lambda = 0$ 永远最优（模型越复杂，训练误差越小）。交叉验证通过评估模型在未见过数据上的表现，避免过拟合，找到真正泛化能力最强的 $\lambda$。

### 8.2 5 折交叉验证流程

将 $n_s$ 个抽样细胞随机划分为 5 个等大（或近似等大）的子集 $F_1, F_2, \dots, F_5$：

1. 对每个 $\lambda \in \Lambda = \{0.001, 0.01, 0.1, 0.5, 1.0, 5.0\}$：
   - 对每个 fold $f = 1, 2, \dots, 5$：
     - 训练集：$\bigcup_{i \neq f} F_i$（4 份用于训练）
     - 验证集：$F_f$（1 份用于验证）
     - 在训练集上拟合 Lasso，在验证集上计算 $RMSE_f^{(f)}$
   - 平均 RMSE：$\overline{RMSE}(\lambda) = \frac{1}{5} \sum_{f=1}^{5} RMSE_f^{(f)}(\lambda)$

2. 选择最优 $\lambda$：

   $$
   \lambda^* = \arg\min_{\lambda \in \Lambda} \overline{RMSE}(\lambda)
   $$

### 8.3 多模块聚合 CV

由于有 $k$ 个基因模块，先对每个模块分别计算验证集 RMSE，然后取所有模块的平均 RMSE 作为该 fold 的 CV 分数：

$$
RMSE_f^{(f)}(\lambda) = \frac{1}{k} \sum_{c=1}^{k} \sqrt{\frac{1}{|F_f|} \sum_{j \in F_f} (y_j^{(c)} - \hat{y}_j^{(c)})^2}
$$

这样选择的 $\lambda$ 对所有模块整体最优。

### 8.4 λ-CV 误差曲线

绘制 $\lambda$（对数轴）与 $\overline{RMSE}$ 的关系图，U 形曲线的最低点对应最优 $\lambda$。同时绘制 OLS 的 CV-RMSE 水平线作为基准参考。

### 8.5 代码实现

```python
kf = KFold(n_splits=5, shuffle=True, random_state=42)

for fold, (train_idx, val_idx) in enumerate(kf.split(T_lf)):
    for lam in lasso_lambdas:
        # train on train_idx, validate on val_idx
        lasso = Lasso(alpha=lam, max_iter=10000, random_state=42)
        lasso.fit(Tp_train, y_train)
        y_pred_val = lasso.predict(Tp_val)
        cv_rmse_fold.append(np.sqrt(mean_squared_error(y_val, y_pred_val)))
    cv_results[lam].append(np.mean(cv_rmse_fold))

best_lam_cv = min(avg_cv_rmse_lasso, key=avg_cv_rmse_lasso.get)
```

---

## 9. 拟合优度与误差分析

### 9.1 决定系数 $R^2$

$R^2$（Coefficient of Determination）衡量拟合曲线对数据变异的解释程度：

$$
\boxed{R^2 = 1 - \frac{\sum_{j=1}^{n_s} (y_j - \hat{y}_j)^2}{\sum_{j=1}^{n_s} (y_j - \bar{y})^2} = 1 - \frac{SS_{\text{res}}}{SS_{\text{tot}}}}
$$

其中：

- $\bar{y} = \frac{1}{n_s} \sum_{j=1}^{n_s} y_j$ — 表达量的样本均值
- $SS_{\text{res}} = \sum (y_j - \hat{y}_j)^2$ — 残差平方和
- $SS_{\text{tot}} = \sum (y_j - \bar{y})^2$ — 总平方和

**解读**：

- $R^2 = 1$：完美拟合，拟合曲线通过所有数据点
- $R^2 = 0$：拟合曲线不比均值线更好
- $R^2 < 0$：拟合曲线比均值线还差（可能模型设定错误）
- 实验中 $R^2 > 0.5$ 视为"显著趋势基因"

### 9.2 均方根误差 RMSE

RMSE（Root Mean Squared Error）以原始量纲衡量拟合的平均偏差：

$$
\boxed{RMSE = \sqrt{\frac{1}{n_s} \sum_{j=1}^{n_s} (y_j - \hat{y}_j)^2} = \sqrt{\frac{SS_{\text{res}}}{n_s}}}
$$

RMSE 越小，拟合越精确。实验中 $RMSE < 0.1$（标准化后的表达量通常在 0–5 之间，此阈值对应约 2%–5% 的平均偏差）视为合格。

### 9.3 残差方差（Residual Variance）

残差方差是 $RSS$ 的无偏估计量，用于检验时间点是否充足：

$$
\boxed{\sigma^2 = \frac{1}{n_s - p - 1} \sum_{j=1}^{n_s} (y_j - \hat{y}_j)^2 = \frac{SS_{\text{res}}}{n_s - p - 1}}
$$

分母 $n_s - p - 1$ 为自由度（$n_s$ 个数据点减去 $p+1$ 个参数），确保 $\sigma^2$ 是真实误差方差 $\sigma_{\text{true}}^2$ 的无偏估计：

$$
\mathbb{E}[\sigma^2] = \sigma_{\text{true}}^2
$$

实验中 $\sigma^2 < 0.05$ 说明时间点数量充足、拟合精度达标。

### 9.4 代码实现

```python
r2 = r2_score(y, y_pred)
rmse = np.sqrt(mean_squared_error(y, y_pred))
residuals = y - y_pred
residual_var = np.sum(residuals**2) / (n_pts - p_params - 1)
```

---

## 10. 假设检验

### 10.1 Pearson 相关性检验——基因表达趋势显著性

#### 10.1.1 Pearson 相关系数

衡量基因表达量 $y$ 与时间 $t$ 之间的线性相关程度：

$$
\boxed{r_{Pearson} = \frac{\sum_{j=1}^{n_s} (t_j - \bar{t})(y_j - \bar{y})}{\sqrt{\sum_{j=1}^{n_s} (t_j - \bar{t})^2} \sqrt{\sum_{j=1}^{n_s} (y_j - \bar{y})^2}}}
$$

$r \in [-1, 1]$：
- $r > 0$：表达随时间上升
- $r < 0$：表达随时间下降
- $r = 0$：无线性相关

#### 10.1.2 显著性检验

- 原假设 $H_0$：$r = 0$（基因表达与时间无关）
- 备择假设 $H_1$：$r \neq 0$（基因表达与时间显著相关）

检验统计量（在 $H_0$ 下服从自由度为 $n_s - 2$ 的 $t$ 分布）：

$$
t = r \sqrt{\frac{n_s - 2}{1 - r^2}} \sim t(n_s - 2)
$$

$p$ 值为双边检验：$p = 2 \cdot P(T > |t|)$，其中 $T \sim t(n_s - 2)$。

决策规则：若 $p < 0.05$，拒绝 $H_0$，认为基因具有显著表达趋势。

### 10.2 Spearman 秩相关——排序合理性验证

#### 10.2.1 Spearman 相关系数

Spearman 相关系数衡量两个变量的**单调**关系（不要求线性），先将数据转换为秩（Rank）再计算 Pearson 相关：

$$
\boxed{\rho_{Spearman} = 1 - \frac{6 \sum d_i^2}{n(n^2 - 1)}}
$$

其中 $d_i = R(t_i) - R(y_i)$ 为第 $i$ 个观测在两个变量上的秩之差（此简化公式仅在无并列时成立；有并列时需用 Pearson 相关公式计算秩之间的相关）。

#### 10.2.2 应用场景

1. **排序单调性检验**：验证阶段内细胞排序序号与驱动模块表达值是否单调一致。若 $|\rho| > 0.8$（$p < 0.05$），排序合理。
2. **轨迹验证**：验证算法排序结果与已知伪时间标签之间的相关性。$\rho > 0.7$ 视为排序合理。

### 10.3 显著趋势基因的综合判定

一个基因模块被判定为"显著趋势模块"需同时满足三个条件：

$$
\begin{cases}
R^2 > 0.5 & \text{（拟合优度足够）} \\
RMSE < 0.1 & \text{（拟合误差较小）} \\
p_{\text{Pearson}} < 0.05 & \text{（表达-时间相关性显著）}
\end{cases}
$$

### 10.4 代码实现

```python
r_pearson, p_pearson = stats.pearsonr(T_lf.ravel(), y)

spearman_r, spearman_p = stats.spearmanr(sorted_order, true_pseudotimes)
```

---

## 11. 负对照实验：时间点随机打乱

### 11.1 实验目的

验证分配的时间点是否真正携带了基因表达的时序信息，排除"任何随机时间点都能得到类似拟合效果"的可能性（即排除过拟合导致的伪轨迹）。

### 11.2 实验设计

1. 保持细胞-表达量的对应关系不变，将时间点向量 $\mathbf{t}$ 随机打乱（shuffle），破坏时间点与细胞之间的真实对应关系
2. 在打乱后的数据上进行相同的最小二乘拟合（$p=3$），计算平均 $R^2$
3. 重复 $N = 100$ 次，得到零分布 $R^2_{\text{shuffle}} = \{R^2_{(1)}, R^2_{(2)}, \dots, R^2_{(100)}\}$
4. 比较原始 $R^2$ 与打乱分布的 95% 分位数

### 11.3 统计判断

若：

$$
R^2_{\text{original}} > Q_{95\%}(R^2_{\text{shuffle}})
$$

即原始 $R^2$ 高于打乱分布的 95% 分位数，以 5% 的显著性水平拒绝"时间点无意义"的原假设，认为轨迹可信。

### 11.4 原理

打乱时间点等价于破坏了基因表达与发育时间之间的因果关系。如果在此条件下仍能得到高 $R^2$，说明原始的高 $R^2$ 可能来自过拟合（多项式足够灵活以至于可以拟合任何随机噪声模式）。反之，若原始 $R^2$ 显著高于所有随机打乱后的 $R^2$，则证明时序信息的真实性。

### 11.5 代码实现

```python
for _ in range(N_SHUFFLE):
    T_shuffled = T_lf.copy()
    np.random.shuffle(T_shuffled)
    # fit and compute R^2
    r2_shuffled_all.append(np.mean(r2_list))

r2_shuffled_threshold = np.percentile(r2_shuffled_all, 95)
# PASS if r2_original_mean > r2_shuffled_threshold
```

---

## 12. 基于投票的细胞轨迹排序

### 12.1 基本思想

利用显著趋势模块的拟合曲线信息，通过"基因投票"机制确定细胞间的相对发育顺序。每个显著趋势基因"投票"决定任意一对细胞的先后关系，最终通过聚合所有投票得到全局细胞顺序。

这种方法**不依赖 PCA 或任何全局降维方法**，避免了循环论证（即用 PCA 得到伪时间再用伪时间验证 PCA）。

### 12.2 投票机制

对于一对细胞 $(j_1, j_2)$ 和基因模块 $g$：

1. 计算模块 $g$ 的拟合值：$\hat{y}_g(t_{j_1})$ 和 $\hat{y}_g(t_{j_2})$
2. 判断模块 $g$ 的整体趋势方向（上升/下降）：

   $$
   \text{trend}(g) = \begin{cases}
   \text{rising} & \text{if } r_{\text{Pearson}}(\mathbf{t}, \hat{\mathbf{y}}_g) > 0 \\
   \text{falling} & \text{if } r_{\text{Pearson}}(\mathbf{t}, \hat{\mathbf{y}}_g) < 0
   \end{cases}
   $$

3. 投票规则：

   $$
   \text{vote}_g(j_1, j_2) = \begin{cases}
   1 & \text{if rising and } \hat{y}_g(t_{j_1}) < \hat{y}_g(t_{j_2}) \\
   1 & \text{if falling and } \hat{y}_g(t_{j_1}) > \hat{y}_g(t_{j_2}) \\
   0 & \text{otherwise}
   \end{cases}
   $$

   即：若基因为上升趋势，表达低的细胞应排在前面；下降趋势则表达高的排在前面。

### 12.3 投票矩阵

构建投票矩阵 $\mathbf{V} \in \mathbb{R}^{n_s \times n_s}$：

$$
V_{j_1, j_2} = \sum_{g \in \mathcal{G}_{\text{sig}}} \text{vote}_g(j_1, j_2)
$$

$V_{j_1, j_2}$ 表示"认为 $j_1$ 应排在 $j_2$ 之前"的基因模块数。

### 12.4 排序聚合

最简单的聚合方式是计算每个细胞的"总得票数"（即投票矩阵的行和），按得票数降序排列：

$$
\text{score}(j) = \sum_{j' \neq j} V_{j, j'}
$$

排序：

$$
\text{order}(j) = \text{argsort}(-\text{score}(j))
$$

更严谨的方式是使用 Kemeny 最优排序（NP-hard）或其近似算法，但对于本实验规模，基于得票数的贪心排序已足够。

### 12.5 只依赖拟合值、不依赖 PCA

这里的关键设计是：排序完全基于**已拟合的多项式曲线在离散时间点上的预测值**，而非原始表达数据的降维表示。拟合曲线本身已经压缩了时序信息，所以排序自然地反映了基因表达的动态变化趋势。

### 12.6 代码实现

```python
vote_matrix = np.zeros((n_sampled, n_sampled))
for mod_id in significant_modules:
    y_pred = all_fitting_results[mod_id]['degree'][3]['y_pred']
    trend_r, _ = stats.pearsonr(T_lf.ravel(), y_pred)
    is_rising = trend_r > 0
    for i in range(n_sampled):
        for j in range(n_sampled):
            if is_rising and y_pred[i] < y_pred[j]:
                vote_matrix[i, j] += 1
            elif not is_rising and y_pred[i] > y_pred[j]:
                vote_matrix[i, j] += 1

cell_scores = vote_matrix.sum(axis=1)
sorted_order = np.argsort(-cell_scores)
```

---

## 13. NMI 与 ARI 轨迹验证

### 13.1 问题

Spearman 相关系数需要连续的伪时间标签进行验证。然而真实数据中的生物学标签通常是离散的阶段标识（如 HSC、MPP、GMP），因此需要基于离散标签的验证方法。

### 13.2 预测阶段划分

将排序后的细胞按已知阶段细胞数比例划分区间。设已知有 $S$ 个阶段，各阶段细胞数为 $n_1, n_2, \dots, n_S$，总细胞数 $N = \sum n_i$：

- 排序后的前 $n_1$ 个细胞 → 预测阶段 1
- 接下来的 $n_2$ 个细胞 → 预测阶段 2
- 依此类推

### 13.3 NMI（归一化互信息）

互信息（Mutual Information, MI）衡量两个随机变量之间的依赖程度：

$$
I(U, V) = \sum_{u \in U} \sum_{v \in V} P(u, v) \log \frac{P(u, v)}{P(u) P(v)}
$$

其中 $P(u, v)$ 为联合概率分布，$P(u)$ 和 $P(v)$ 为边际分布，均从数据中通过频率估计。

NMI 对互信息进行归一化，使其取值在 $[0, 1]$：

$$
\boxed{NMI(U, V) = \frac{2 \cdot I(U, V)}{H(U) + H(V)}}
$$

其中 $H(U) = -\sum_u P(u) \log P(u)$ 为香农熵。

NMI = 1 表示完美一致，NMI = 0 表示完全无关。实验中 $NMI > 0.6$ 视为排序合理。

### 13.4 ARI（调整兰德指数）

兰德指数（Rand Index, RI）衡量两个聚类/划分的一致性：

$$
RI = \frac{\text{一致的对数}}{\text{总对数}} = \frac{a + b}{\binom{n}{2}}
$$

其中 $a$ 为在真实和预测划分中都属于同一类的细胞对数，$b$ 为在两者中都不属于同一类的细胞对数。

调整兰德指数（ARI）对 RI 进行"调整"，矫正随机匹配带来的偏差：

$$
\boxed{ARI = \frac{RI - \mathbb{E}[RI]}{\max(RI) - \mathbb{E}[RI]}}
$$

ARI 范围 $[-1, 1]$：
- ARI = 1：完全一致
- ARI = 0：等价于随机划分
- ARI < 0：比随机划分还差（对立的划分结构）

实验中 $ARI > 0.5$ 视为排序合理。

### 13.5 综合判定

同时满足 $NMI > 0.6$ 和 $ARI > 0.5$ 时，认为轨迹排序合理。

### 13.6 代码实现

```python
from sklearn.metrics import normalized_mutual_info_score, adjusted_rand_score

nmi = normalized_mutual_info_score(true_stages_sampled, predicted_stages)
ari = adjusted_rand_score(true_stages_sampled, predicted_stages)
```

---

## 14. 数值实现细节

### 14.1 多项式特征构造与截距处理

scikit-learn 的 `PolynomialFeatures(include_bias=False)` 生成不含全 1 列的设计矩阵，而 `LinearRegression(fit_intercept=True)` 自行添加截距项。这样避免了设计矩阵中出现两列全 1（一列来自 `PolynomialFeatures`，一列来自 `fit_intercept`）导致的矩阵奇异问题。

对于一次多项式（degree=1），`include_bias=False` 时设计矩阵只含 $[t]$，加上 `fit_intercept=True` 后等价于 $[1, t]$，正确。

### 14.2 数值稳定性

- **对数变换**：使用 `np.log1p(x)` 而非 `np.log(1 + x)`，在 $x \approx 0$ 时更精确（避免浮点舍入误差）
- **除零保护**：CV 计算中分母加 $\varepsilon = 10^{-8}$
- **Lasso 收敛**：设置 `max_iter=10000` 确保坐标下降法充分收敛
- **随机种子**：固定 `random_state=42` 保证结果可复现
- **KFold shuffle**：`shuffle=True` 配合固定 random_state 确保交叉验证的一致性

### 14.3 并行与性能优化

```python
os.environ['LOKY_MAX_CPU_COUNT'] = '4'
os.environ['OMP_NUM_THREADS'] = '1'
os.environ['OPENBLAS_NUM_THREADS'] = '1'
os.environ['MKL_NUM_THREADS'] = '1'
```

这些环境变量限制了底层线性代数库的线程数，避免了 scikit-learn 并行（通过 loky）与 BLAS 多线程之间的竞争，防止 CPU 过度订阅。

### 14.4 数据读取

使用 `engine='calamine'`（python-calamine 库）读取 Excel 文件，相比默认的 openpyxl 引擎速度更快（特别是对大型表达矩阵）。

### 14.5 双分支对称处理

在拟合阶段，Left 和 Right 两个分支使用的是完全相同的拟合流程，独立处理。主要分析指标（$R^2$、RMSE、Pearson 检验）在 Left 分支上报告，Right 分支的拟合结果同样保存在 `branch_results` 中供进一步分析。交叉验证选择的最优 $\lambda$ 同时应用于两个分支的 Lasso 拟合。

### 14.6 抽样策略的数学保证

均匀抽样确保了：
1. 采样点覆盖模块表达的全量程范围（从最低到最高），避免外推误差
2. 时间点均匀分布在阶段区间内，满足多项式拟合对自变量分布的基本要求
3. 抽样量 $n_s \geq 3p + 1$ 保证正规方程 $\mathbf{T}^T\mathbf{T}$ 的可逆性和参数估计的统计效率

### 14.7 从抽样细胞到全体细胞的扩展（选做）

对于已拟合的模块曲线，可通过以下策略将排序推广到全体细胞：

**策略 A（插值法）**：对全体细胞中的每个细胞 $j$，计算其与所有抽样细胞在显著趋势模块表达上的欧氏距离，取最近 $k=5$ 个抽样细胞伪时间的距离加权平均：

$$
\hat{t}_j = \frac{\sum_{i \in \mathcal{N}_k(j)} w_i t_i}{\sum_{i \in \mathcal{N}_k(j)} w_i},\quad w_i = \frac{1}{\|\mathbf{e}_j - \mathbf{e}_i\| + \varepsilon}
$$

**策略 B（模型预测）**：以抽样细胞的伪时间为标签，显著趋势模块表达为特征，训练随机森林回归器 $\hat{f}$，预测全体细胞的伪时间 $\hat{t}_j = \hat{f}(\mathbf{e}_j)$。

---

## 附录：关键公式速查表

| 公式          | 表达式                                                                                                 | 用途             |
| ------------- | ------------------------------------------------------------------------------------------------------ | ---------------- |
| 变异系数      | $CV_i = \sigma_i / (\mu_i + \varepsilon)$                                                              | HVG 筛选         |
| 对数标准化    | $X_{ij}^{\text{norm}} = \ln(1 + \frac{X_{ij}}{\sum_k X_{kj}} \times 10000)$                            | 消除测序深度差异 |
| K-means 目标  | $SSE = \sum_{c=1}^{k} \sum_{\mathbf{g}_i \in C_c} \|\mathbf{g}_i - \boldsymbol{\mu}_c\|^2$             | 基因聚类         |
| 轮廓系数      | $s(i) = \frac{b(i) - a(i)}{\max(a(i), b(i))}$                                                          | 最优 $k$ 选择    |
| 时间点插值    | $t_{ij} = t_i^{\text{start}} + \frac{j-1}{n_s - 1}(t_i^{\text{end}} - t_i^{\text{start}})$             | 连续时间分配     |
| OLS 解析解    | $\mathbf{a}^* = (\mathbf{T}^T\mathbf{T})^{-1}\mathbf{T}^T\mathbf{y}$                                   | 多项式拟合       |
| Lasso 目标    | $\min_{\mathbf{a}} \{ RSS + \lambda \sum_{m=1}^{p} \|a_m\| \}$                                         | 正则化拟合       |
| 决定系数      | $R^2 = 1 - SS_{\text{res}} / SS_{\text{tot}}$                                                          | 拟合优度         |
| 均方根误差    | $RMSE = \sqrt{SS_{\text{res}} / n_s}$                                                                  | 拟合精度         |
| 残差方差      | $\sigma^2 = SS_{\text{res}} / (n_s - p - 1)$                                                           | 时间点充足性     |
| Pearson 相关  | $r = \frac{\sum (t_j - \bar{t})(y_j - \bar{y})}{\sqrt{\sum (t_j - \bar{t})^2 \sum (y_j - \bar{y})^2}}$ | 趋势显著性       |
| Spearman 相关 | $\rho = 1 - \frac{6\sum d_i^2}{n(n^2-1)}$                                                              | 单调性/排序验证  |
| NMI           | $NMI = \frac{2I(U,V)}{H(U)+H(V)}$                                                                      | 离散阶段一致性   |
| ARI           | $ARI = \frac{RI - \mathbb{E}[RI]}{\max(RI) - \mathbb{E}[RI]}$                                          | 调整的聚类一致性 |

---

*本文档涵盖了实验三涉及的所有核心数学原理，从数据预处理（HVG 筛选、标准化、K-means 聚类）到核心分析（最小二乘拟合、Lasso 正则化、交叉验证）再到验证方法（假设检验、负对照实验、NMI/ARI）。建议结合 `ex.md`（实验指导）、`experiment3_part1_preprocessing.py` 和 `experiment3_part2_fitting.py` 对照阅读。*
