import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.interpolate import interp1d, CubicSpline, Rbf
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# 设置matplotlib中文字体支持
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False
sns.set_style('whitegrid')

# ==================== 1. 数据加载和预处理 ====================
def load_stock_data():
    """
    加载历史行情数据
    """
    try:
        # 读取上传的Excel文件
        df_a = pd.read_excel('历史行情模型A.xlsx')
        df_b = pd.read_excel('历史行情模型B.xlsx')
        
        print("成功加载历史行情数据文件")
        print(f"模型A数据形状: {df_a.shape}")
        print(f"模型B数据形状: {df_b.shape}")
        
        # 合并或选择一个文件作为基础数据
        # 假设模型B包含更完整的贵州茅台数据
        if 'close' in df_b.columns or '收盘价' in df_b.columns:
            df = df_b.copy()
        else:
            df = df_a.copy()
        
        # 标准化列名
        column_mapping = {
            '日期': 'date',
            '时间': 'date',
            'datetime': 'date',
            '收盘价': 'close',
            'close': 'close',
            'Close': 'close'
        }
        
        df = df.rename(columns=column_mapping)
        
        # 确保日期列存在
        if 'date' not in df.columns:
            # 尝试其他可能的日期列名
            date_cols = [col for col in df.columns if 'date' in col.lower() or 'time' in col.lower()]
            if date_cols:
                df = df.rename(columns={date_cols[0]: 'date'})
            else:
                # 使用索引作为日期
                df['date'] = pd.date_range(start='2024-01-01', periods=len(df), freq='B')
        
        # 确保收盘价列存在
        if 'close' not in df.columns:
            price_cols = [col for col in df.columns if 'price' in col.lower() or 'close' in col.lower()]
            if price_cols:
                df = df.rename(columns={price_cols[0]: 'close'})
            else:
                print("警告：未找到收盘价列，使用第一列数值数据")
                numeric_cols = df.select_dtypes(include=[np.number]).columns
                if numeric_cols.any():
                    df['close'] = df[numeric_cols[0]]
        
        # 转换日期列
        if not pd.api.types.is_datetime64_any_dtype(df['date']):
            df['date'] = pd.to_datetime(df['date'])
        
        # 按日期排序
        df = df.sort_values('date')
        
        # 选择100个交易日
        if len(df) > 100:
            df = df.iloc[-100:]  # 取最近100天
        
        # 重置索引
        df = df.reset_index(drop=True)
        
        print(f"最终使用的数据: {len(df)}个交易日")
        print(f"日期范围: {df['date'].min().strftime('%Y-%m-%d')} 到 {df['date'].max().strftime('%Y-%m-%d')}")
        print(f"价格范围: {df['close'].min():.2f} - {df['close'].max():.2f}")
        
        return df[['date', 'close']]
    
    except Exception as e:
        print(f"数据加载错误: {e}")
        print("使用模拟的贵州茅台数据作为替代...")
        return generate_mock_guizhou_maotai_data()

def generate_mock_guizhou_maotai_data():
    """
    生成模拟的贵州茅台数据
    """
    dates = pd.date_range(start='2024-01-01', periods=100, freq='B')  # 100个交易日
    np.random.seed(42)
    
    # 模拟贵州茅台股价特征
    base_price = 1700
    trend = np.linspace(0, 80, 100)  # 上升趋势
    seasonal = np.sin(np.linspace(0, 4*np.pi, 100)) * 30  # 季节性波动
    noise = np.random.normal(0, 15, 100)  # 随机噪声
    volatility = np.zeros(100)
    
    # 添加一些波动性特征
    for i in range(100):
        if 30 <= i <= 40:  # 中期波动
            volatility[i] = np.sin((i-30) * np.pi/5) * 50
        if 70 <= i <= 80:  # 后期波动
            volatility[i] = np.sin((i-70) * np.pi/5) * 70
    
    prices = base_price + trend + seasonal + noise + volatility
    
    df = pd.DataFrame({
        'date': dates,
        'close': prices
    })
    
    return df

# ==================== 2. 缺失模式构造 ====================
def create_missing_patterns(df):
    """
    创建两种缺失模式
    """
    df_missing_a = df.copy()
    df_missing_b = df.copy()
    
    # 模式A: 均匀间隔缺失（每隔4天缺1天）
    missing_indices_a = [i for i in range(len(df)) if i % 5 != 0]  # 保留第1、6、11、16...天
    df_missing_a.loc[missing_indices_a, 'close'] = np.nan
    
    # 模式B: 密集区域缺失（连续10天内只保留首尾两天）
    # 选择中间时间段（避免边界效应）
    start_idx = 40  # 从第40天开始
    end_idx = start_idx + 9  # 连续10天（包含首尾）
    
    if end_idx >= len(df):
        end_idx = len(df) - 1
        start_idx = end_idx - 9
    
    # 只保留首尾两天，中间8天设为缺失
    missing_indices_b = list(range(start_idx + 1, end_idx))
    df_missing_b.loc[missing_indices_b, 'close'] = np.nan
    
    print(f"模式A: 均匀间隔缺失 - 缺失率: {len(missing_indices_a)/len(df):.1%}")
    print(f"保留的日期: {df.iloc[::5]['date'].dt.strftime('%Y-%m-%d').tolist()[:5]}...")
    
    print(f"\n模式B: 密集区域缺失 - 时间段: {df.iloc[start_idx]['date'].strftime('%Y-%m-%d')} 到 {df.iloc[end_idx]['date'].strftime('%Y-%m-%d')}")
    print(f"缺失率: {len(missing_indices_b)/len(df):.1%}")
    print(f"保留的日期: {df.iloc[start_idx]['date'].strftime('%Y-%m-%d')}, {df.iloc[end_idx]['date'].strftime('%Y-%m-%d')}")
    
    return df_missing_a, df_missing_b, missing_indices_a, missing_indices_b, start_idx, end_idx

# ==================== 3. 插值方法实现 ====================
class InterpolationMethods:
    """
    插值方法集合
    """
    
    @staticmethod
    def piecewise_linear(x_known, y_known, x_all):
        """
        分段线性插值 - 使用scipy.interpolate.interp1d
        """
        # 创建插值函数
        interp_func = interp1d(x_known, y_known, kind='linear', fill_value='extrapolate')
        return interp_func(x_all)
    
    @staticmethod
    def cubic_spline(x_known, y_known, x_all):
        """
        三次样条插值
        """
        cs = CubicSpline(x_known, y_known, bc_type='natural')
        return cs(x_all)
    
    @staticmethod
    def rbf_interpolation(x_known, y_known, x_all):
        """
        径向基函数插值
        """
        rbf = Rbf(x_known, y_known, function='multiquadric', epsilon=0.1)
        return rbf(x_all)
    
    @staticmethod
    def forward_fill(x_known, y_known, x_all):
        """
        前向填充（基准方法）
        """
        result = np.zeros_like(x_all)
        known_dict = dict(zip(x_known, y_known))
        
        last_value = None
        for i, x in enumerate(x_all):
            if x in known_dict:
                last_value = known_dict[x]
            result[i] = last_value if last_value is not None else y_known[0]
        
        return result

# ==================== 4. 5日均线和信号分析 ====================
def calculate_ma5(prices, window=5):
    """
    计算5日移动平均线
    """
    return pd.Series(prices).rolling(window=window, min_periods=1).mean().values

def generate_trading_signals(prices, ma5):
    """
    生成交易信号
    规则：价格上穿5日均线时买入，下穿时卖出
    """
    signals = np.zeros(len(prices))
    
    for i in range(1, len(prices)):
        # 买入信号：价格上穿5日均线
        if prices[i] > ma5[i] and prices[i-1] <= ma5[i-1]:
            signals[i] = 1
        # 卖出信号：价格下穿5日均线
        elif prices[i] < ma5[i] and prices[i-1] >= ma5[i-1]:
            signals[i] = -1
    
    return signals

def analyze_signal_differences(signal_base, signal_interp, method_name):
    """
    分析信号差异
    """
    diff_indices = np.where(signal_base != signal_interp)[0]
    diff_count = len(diff_indices)
    
    if diff_count == 0:
        return {
            'method': method_name,
            'diff_count': 0,
            'false_signals': 0,
            'missed_signals': 0,
            'analysis': '信号完全一致，无差异'
        }
    
    # 分析差异类型
    false_signals = 0  # 虚假信号：基准无信号，插值有信号
    missed_signals = 0  # 漏失信号：基准有信号，插值无信号
    
    for idx in diff_indices:
        if signal_base[idx] == 0 and signal_interp[idx] != 0:
            false_signals += 1
        elif signal_base[idx] != 0 and signal_interp[idx] == 0:
            missed_signals += 1
    
    analysis = f"信号差异: {diff_count}处\n"
    analysis += f"- 虚假信号: {false_signals}个\n"
    analysis += f"- 漏失信号: {missed_signals}个"
    
    return {
        'method': method_name,
        'diff_count': diff_count,
        'false_signals': false_signals,
        'missed_signals': missed_signals,
        'analysis': analysis
    }

# ==================== 5. 评估和分析函数 ====================
def evaluate_interpolation_methods(df_full, df_missing_a, df_missing_b, start_idx, end_idx):
    """
    评估各种插值方法
    """
    results = {}
    
    # 准备完整数据
    x_all = np.arange(len(df_full))
    y_true = df_full['close'].values
    
    # 定义插值方法
    methods = {
        '分段线性插值': InterpolationMethods.piecewise_linear,
        '三次样条插值': InterpolationMethods.cubic_spline,
        '径向基函数插值': InterpolationMethods.rbf_interpolation,
        '前向填充(基准)': InterpolationMethods.forward_fill
    }
    
    # 评估每种缺失模式
    for pattern_name, df_missing in [('模式A', df_missing_a), ('模式B', df_missing_b)]:
        print(f"\n{'='*60}")
        print(f"评估 {pattern_name}")
        print(f"{'='*60}")
        
        # 找出缺失值的位置
        missing_mask = df_missing['close'].isna().values
        known_mask = ~missing_mask
        
        x_known = x_all[known_mask]
        y_known = df_missing['close'].values[known_mask]
        
        pattern_results = {}
        
        for method_name, method_func in methods.items():
            print(f"  处理 {method_name}...")
            
            # 应用插值
            y_interp = method_func(x_known, y_known, x_all)
            
            # 计算RMSE（仅在缺失位置计算）
            rmse = np.sqrt(np.mean((y_true[missing_mask] - y_interp[missing_mask]) ** 2))
            
            # 计算5日均线
            ma5_interp = calculate_ma5(y_interp)
            ma5_true = calculate_ma5(y_true)
            
            # 生成交易信号
            signals_interp = generate_trading_signals(y_interp, ma5_interp)
            signals_true = generate_trading_signals(y_true, ma5_true)
            
            # 分析信号差异
            signal_analysis = analyze_signal_differences(signals_true, signals_interp, method_name)
            
            pattern_results[method_name] = {
                'interpolated_values': y_interp,
                'rmse': rmse,
                'ma5': ma5_interp,
                'signals': signals_interp,
                'signal_analysis': signal_analysis,
                'known_indices': x_known
            }
            
            print(f"    RMSE: {rmse:.4f}")
            print(f"    {signal_analysis['analysis']}")
        
        results[pattern_name] = pattern_results
    
    return results

# ==================== 6. 可视化函数 ====================
def plot_interpolation_results(df_full, df_missing_a, df_missing_b, results, start_idx, end_idx):
    """
    绘制插值结果对比图
    """
    plt.figure(figsize=(15, 12))
    
    # 1. 模式A：均匀间隔缺失
    plt.subplot(2, 1, 1)
    plt.plot(df_full['date'], df_full['close'], 'b-', linewidth=2, label='真实价格', alpha=0.8)
    plt.plot(df_full['date'], df_missing_a['close'], 'ro', markersize=4, label='观测值', alpha=0.7)
    
    colors = ['g', 'm', 'c', 'y']
    for i, (method_name, result) in enumerate(results['模式A'].items()):
        plt.plot(df_full['date'], result['interpolated_values'], 
                f'{colors[i]}--', linewidth=1.5, 
                label=f'{method_name} (RMSE: {result["rmse"]:.2f})')
    
    plt.title('模式A：均匀间隔缺失 - 插值方法对比', fontsize=14, fontweight='bold')
    plt.xlabel('日期', fontsize=12)
    plt.ylabel('收盘价', fontsize=12)
    plt.legend(loc='best')
    plt.grid(True, alpha=0.3)
    
    # 2. 模式B：密集区域缺失
    plt.subplot(2, 1, 2)
    plt.plot(df_full['date'], df_full['close'], 'b-', linewidth=2, label='真实价格', alpha=0.8)
    plt.plot(df_full['date'], df_missing_b['close'], 'ro', markersize=4, label='观测值', alpha=0.7)
    
    for i, (method_name, result) in enumerate(results['模式B'].items()):
        plt.plot(df_full['date'], result['interpolated_values'], 
                f'{colors[i]}--', linewidth=1.5, 
                label=f'{method_name} (RMSE: {result["rmse"]:.2f})')
    
    # 标记密集缺失区域
    plt.axvspan(df_full.iloc[start_idx]['date'], df_full.iloc[end_idx]['date'], 
               color='red', alpha=0.1, label='密集缺失区域')
    
    plt.title('模式B：密集区域缺失 - 插值方法对比', fontsize=14, fontweight='bold')
    plt.xlabel('日期', fontsize=12)
    plt.ylabel('收盘价', fontsize=12)
    plt.legend(loc='best')
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('插值方法对比.png', dpi=300, bbox_inches='tight')
    plt.show()

def plot_ma5_comparison(df_full, results):
    """
    绘制5日均线对比图
    """
    plt.figure(figsize=(15, 10))
    
    # 模式A
    plt.subplot(2, 1, 1)
    ma5_true = calculate_ma5(df_full['close'].values)
    plt.plot(df_full['date'], ma5_true, 'b-', linewidth=2, label='真实5日均线', alpha=0.8)
    
    for method_name, result in results['模式A'].items():
        plt.plot(df_full['date'], result['ma5'], '--', linewidth=1.5, 
                label=f'{method_name} 5日均线')
    
    plt.title('模式A：5日均线对比', fontsize=14, fontweight='bold')
    plt.xlabel('日期', fontsize=12)
    plt.ylabel('5日均线', fontsize=12)
    plt.legend(loc='best')
    plt.grid(True, alpha=0.3)
    
    # 模式B
    plt.subplot(2, 1, 2)
    plt.plot(df_full['date'], ma5_true, 'b-', linewidth=2, label='真实5日均线', alpha=0.8)
    
    for method_name, result in results['模式B'].items():
        plt.plot(df_full['date'], result['ma5'], '--', linewidth=1.5, 
                label=f'{method_name} 5日均线')
    
    plt.title('模式B：5日均线对比', fontsize=14, fontweight='bold')
    plt.xlabel('日期', fontsize=12)
    plt.ylabel('5日均线', fontsize=12)
    plt.legend(loc='best')
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('5日均线对比.png', dpi=300, bbox_inches='tight')
    plt.show()

def plot_signal_analysis(df_full, results):
    """
    绘制交易信号分析图
    """
    plt.figure(figsize=(15, 8))
    
    # 真实价格和信号
    plt.plot(df_full['date'], df_full['close'], 'b-', linewidth=2, label='真实价格', alpha=0.8)
    
    # 真实信号
    ma5_true = calculate_ma5(df_full['close'].values)
    signals_true = generate_trading_signals(df_full['close'].values, ma5_true)
    
    buy_dates = df_full['date'][signals_true == 1]
    sell_dates = df_full['date'][signals_true == -1]
    buy_prices = df_full['close'][signals_true == 1]
    sell_prices = df_full['close'][signals_true == -1]
    
    plt.scatter(buy_dates, buy_prices, marker='^', color='g', s=100, label='真实买入信号')
    plt.scatter(sell_dates, sell_prices, marker='v', color='r', s=100, label='真实卖出信号')
    
    # 模式B的差异信号（更关键）
    for method_name, result in results['模式B'].items():
        signal_analysis = result['signal_analysis']
        if signal_analysis['diff_count'] > 0:
            diff_indices = np.where(signals_true != result['signals'])[0]
            diff_dates = df_full['date'].iloc[diff_indices]
            diff_prices = df_full['close'].iloc[diff_indices]
            
            plt.scatter(diff_dates, diff_prices, marker='o', s=80, 
                       label=f'{method_name} 差异信号({signal_analysis["diff_count"]})',
                       alpha=0.7)
    
    plt.title('模式B：交易信号差异分析（密集缺失区域）', fontsize=14, fontweight='bold')
    plt.xlabel('日期', fontsize=12)
    plt.ylabel('收盘价', fontsize=12)
    plt.legend(loc='best')
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('信号差异分析.png', dpi=300, bbox_inches='tight')
    plt.show()

# ==================== 7. 表格生成函数 ====================
def create_missing_pattern_table():
    """
    创建缺失模式设计表
    """
    pattern_data = {
        '模式编号': ['模式A', '模式B'],
        '缺失特点': [
            '均匀间隔缺失（每隔4天缺失1天）',
            '密集区域缺失（连续10天内只保留首尾两天）'
        ],
        '示例（选点方法）': [
            '保留第1、6、11、16、21、26、31、36、41、46...天\n（即索引 % 5 == 0 的日期）',
            '在中间连续10天内（如第40-49天）\n仅保留第40天和第49天数据\n（中间8天全部缺失）'
        ],
        '缺失率': ['80%\n（100个交易日中缺失80天）', '8%\n（100个交易日中缺失8天）'],
        '考察特性': [
            '1. 全局平滑性\n2. 长期趋势捕捉能力\n3. 龙格现象抑制能力',
            '1. 局部波动捕捉能力\n2. 短期剧烈变化适应性\n3. 边界条件处理能力'
        ]
    }
    
    pattern_df = pd.DataFrame(pattern_data)
    
    # 保存表格
    pattern_df.to_csv('缺失模式设计表.csv', index=False, encoding='utf_8_sig')
    pattern_df.to_excel('缺失模式设计表.xlsx', index=False)
    
    print("\n" + "="*80)
    print("表1：缺失模式设计表")
    print("="*80)
    print(pattern_df.to_string(index=False))
    
    return pattern_df

def create_interpolation_results_table(results):
    """
    创建插值结果分析表
    """
    table_data = []
    
    for pattern_name in ['模式A', '模式B']:
        for method_name, result in results[pattern_name].items():
            signal_analysis = result['signal_analysis']
            table_data.append({
                '缺失模式': pattern_name,
                '插值方法': method_name,
                'RMSE': f"{result['rmse']:.4f}",
                '信号差异数量': signal_analysis['diff_count'],
                '虚假信号数量': signal_analysis['false_signals'],
                '漏失信号数量': signal_analysis['missed_signals'],
                '信号差异分析': signal_analysis['analysis'].replace('\n', '; ')
            })
    
    results_df = pd.DataFrame(table_data)
    
    # 保存表格
    results_df.to_csv('插值结果分析表.csv', index=False, encoding='utf_8_sig')
    results_df.to_excel('插值结果分析表.xlsx', index=False)
    
    print("\n" + "="*80)
    print("表2：插值结果分析表")
    print("="*80)
    print(results_df.to_string(index=False))
    
    return results_df

# ==================== 8. 生成报告和建议 ====================
def generate_trading_recommendations(results):
    """
    生成交易导向的插值策略建议
    """
    recommendations = []
    
    print("\n" + "="*80)
    print("交易导向的插值策略建议")
    print("="*80)
    
    # 模式A分析
    print("\n## 模式A：均匀间隔缺失（80%缺失率）")
    
    rmse_a = {method: result['rmse'] for method, result in results['模式A'].items()}
    best_method_a = min(rmse_a, key=rmse_a.get)
    
    print(f"• 最佳精度方法: {best_method_a} (RMSE: {rmse_a[best_method_a]:.4f})")
    
    signal_diff_a = {method: result['signal_analysis']['diff_count'] 
                    for method, result in results['模式A'].items()}
    best_signal_a = min(signal_diff_a, key=signal_diff_a.get)
    
    print(f"• 最佳信号保真度: {best_signal_a} ({signal_diff_a[best_signal_a]}个差异信号)")
    
    if best_method_a == best_signal_a:
        recommendations.append({
            '场景': '均匀间隔缺失（高缺失率）',
            '推荐方法': best_method_a,
            '理由': f'在高缺失率下同时提供最佳精度({rmse_a[best_method_a]:.4f})和信号保真度({signal_diff_a[best_method_a]}个差异)',
            '适用策略': '趋势跟踪策略，长期投资'
        })
        print(f"✓ 推荐: {best_method_a} - 适用于趋势跟踪策略")
    else:
        recommendations.append({
            '场景': '均匀间隔缺失（高缺失率）',
            '推荐方法': best_signal_a,
            '理由': f'虽然RMSE略高({rmse_a[best_signal_a]:.4f})，但信号保真度最佳({signal_diff_a[best_signal_a]}个差异),交易信号更重要',
            '适用策略': '趋势跟踪策略，长期投资'
        })
        print(f"✓ 推荐: {best_signal_a} - 交易信号保真度优先")
    
    # 模式B分析
    print("\n## 模式B：密集区域缺失（8%缺失率，关键区域）")
    
    rmse_b = {method: result['rmse'] for method, result in results['模式B'].items()}
    best_method_b = min(rmse_b, key=rmse_b.get)
    
    print(f"• 最佳精度方法: {best_method_b} (RMSE: {rmse_b[best_method_b]:.4f})")
    
    signal_diff_b = {method: result['signal_analysis']['diff_count'] 
                    for method, result in results['模式B'].items()}
    best_signal_b = min(signal_diff_b, key=signal_diff_b.get)
    
    print(f"• 最佳信号保真度: {best_signal_b} ({signal_diff_b[best_signal_b]}个差异信号)")
    
    # 模式B更关注信号差异
    if signal_diff_b[best_signal_b] == 0:
        recommendations.append({
            '场景': '密集区域缺失（关键市场时段）',
            '推荐方法': best_signal_b,
            '理由': f'完美保持信号一致性(0个差异),在关键市场时段避免虚假交易信号至关重要',
            '适用策略': '高频交易，事件驱动策略，风险管理'
        })
        print(f"✓ 推荐: {best_signal_b} - 关键时段信号保真度100%")
    else:
        recommendations.append({
            '场景': '密集区域缺失（关键市场时段）',
            '推荐方法': best_signal_b,
            '理由': f'最小化信号差异({signal_diff_b[best_signal_b]}个),在市场恐慌期避免产生危险的反向信号',
            '适用策略': '高频交易，事件驱动策略，风险管理'
        })
        print(f"✓ 推荐: {best_signal_b} - 最小化关键时段信号风险")
    
    # 通用建议
    print("\n## 通用实施建议")
    print("• 混合策略框架: 根据缺失模式和市场状态动态选择插值方法")
    print("• 风险控制: 设置RMSE阈值(>3%)和信号差异阈值(>2个)触发人工审核")
    print("• 实时监控: 建立插值质量评估机制，记录每次插值的置信度")
    
    recommendations_df = pd.DataFrame(recommendations)
    recommendations_df.to_csv('插值策略建议.csv', index=False, encoding='utf_8_sig')
    recommendations_df.to_excel('插值策略建议.xlsx', index=False)
    
    return recommendations_df

# ==================== 9. 主执行函数 ====================
def main():
    """
    主执行函数
    """
    print("=== 量化交易插值策略研究 ===")
    
    # 1. 加载数据
    print("\n1. 加载历史行情数据...")
    df_full = load_stock_data()
    
    # 2. 创建缺失模式
    print("\n2. 创建缺失模式...")
    df_missing_a, df_missing_b, missing_indices_a, missing_indices_b, start_idx, end_idx = create_missing_patterns(df_full)
    
    # 3. 评估插值方法
    print("\n3. 评估插值方法...")
    results = evaluate_interpolation_methods(df_full, df_missing_a, df_missing_b, start_idx, end_idx)
    
    # 4. 可视化结果
    print("\n4. 生成可视化图表...")
    plot_interpolation_results(df_full, df_missing_a, df_missing_b, results, start_idx, end_idx)
    plot_ma5_comparison(df_full, results)
    plot_signal_analysis(df_full, results)
    
    # 5. 生成表格
    print("\n5. 生成分析表格...")
    pattern_table = create_missing_pattern_table()
    results_table = create_interpolation_results_table(results)
    
    # 6. 生成交易建议
    print("\n6. 生成交易策略建议...")
    recommendations = generate_trading_recommendations(results)
    
    # 7. 保存完整数据
    print("\n7. 保存完整分析数据...")
    
    # 创建完整结果DataFrame
    full_results = df_full.copy()
    full_results['真实5日均线'] = calculate_ma5(df_full['close'].values)
    full_results['真实信号'] = generate_trading_signals(
        df_full['close'].values, 
        full_results['真实5日均线'].values
    )
    
    for pattern_name in ['模式A', '模式B']:
        for method_name, result in results[pattern_name].items():
            suffix = pattern_name.replace('模式', '')
            full_results[f'{method_name}_插值_{suffix}'] = result['interpolated_values']
            full_results[f'{method_name}_5日均线_{suffix}'] = result['ma5']
            full_results[f'{method_name}_信号_{suffix}'] = result['signals']
    
    full_results.to_csv('完整分析数据.csv', index=False, encoding='utf_8_sig')
    full_results.to_excel('完整分析数据.xlsx', index=False)
    
    print("\n" + "="*80)
    print("任务完成！所有文件已生成：")
    print("- 插值方法对比.png")
    print("- 5日均线对比.png")
    print("- 信号差异分析.png")
    print("- 缺失模式设计表.csv/.xlsx")
    print("- 插值结果分析表.csv/.xlsx")
    print("- 插值策略建议.csv/.xlsx")
    print("- 完整分析数据.csv/.xlsx")
    print("="*80)

# ==================== 10. 执行程序 ====================
if __name__ == "__main__":
    # 检查必要库
    required_packages = ['pandas', 'numpy', 'matplotlib', 'seaborn', 'scipy']
    print("确保已安装必要库: " + ", ".join(required_packages))
    print("如未安装，请使用: pip install pandas numpy matplotlib seaborn scipy")
    
    try:
        main()
    except ImportError as e:
        print(f"缺少必要库: {e}")
        print("请安装所需库后重试")
    except Exception as e:
        print(f"程序执行错误: {e}")
        print("尝试使用基本功能...")
        
        # 尝试生成表格
        try:
            create_missing_pattern_table()
            print("缺失模式设计表已生成")
        except Exception as inner_e:
            print(f"表格生成失败: {inner_e}")