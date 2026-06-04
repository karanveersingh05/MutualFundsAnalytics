import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress
import nbformat as nbf
import os
import warnings
warnings.filterwarnings('ignore')

processed_dir = '../data/processed'
charts_dir = '../reports/charts'
os.makedirs(charts_dir, exist_ok=True)

print("Loading data...")
df_nav = pd.read_csv(f'{processed_dir}/02_nav_history_clean.csv', parse_dates=['date'])
df_fund = pd.read_csv(f'{processed_dir}/01_fund_master_clean.csv')
df_bench = pd.read_csv(f'{processed_dir}/10_benchmark_indices_clean.csv', parse_dates=['date'])

# 1. Compute Daily Returns
print("Computing metrics...")
df_nav = df_nav.sort_values(['amfi_code', 'date'])
df_nav['daily_return'] = df_nav.groupby('amfi_code')['nav'].pct_change()

# Nifty 100 and Nifty 50 daily returns
df_bench_100 = df_bench[df_bench['index_name'] == 'NIFTY100'].sort_values('date')
df_bench_100['bench_return'] = df_bench_100['close_value'].pct_change()

df_bench_50 = df_bench[df_bench['index_name'] == 'NIFTY50'].sort_values('date')
df_bench_50['bench_return_50'] = df_bench_50['close_value'].pct_change()

# Join benchmark returns to nav
df_nav = df_nav.merge(df_bench_100[['date', 'bench_return']], on='date', how='left')
df_nav = df_nav.merge(df_bench_50[['date', 'bench_return_50']], on='date', how='left')

results = []
Rf = 0.065
Rf_daily = Rf / 252

for code, group in df_nav.groupby('amfi_code'):
    group = group.dropna(subset=['daily_return'])
    if len(group) == 0:
        continue
    
    start_val = group['nav'].iloc[0]
    end_val = group['nav'].iloc[-1]
    
    if len(group) >= 252:
        val_1y = group['nav'].iloc[-252]
        cagr_1y = (end_val / val_1y) - 1
    else:
        cagr_1y = np.nan
        
    if len(group) >= 252 * 3:
        val_3y = group['nav'].iloc[-252*3]
        cagr_3y = (end_val / val_3y) ** (1/3) - 1
    else:
        cagr_3y = np.nan
        
    if len(group) >= 252 * 5:
        val_5y = group['nav'].iloc[-252*5]
        cagr_5y = (end_val / val_5y) ** (1/5) - 1
    else:
        cagr_5y = np.nan
        
    mean_ret = group['daily_return'].mean()
    std_ret = group['daily_return'].std()
    sharpe = (mean_ret - Rf_daily) / std_ret * np.sqrt(252) if std_ret > 0 else 0
    
    downside_ret = group[group['daily_return'] < 0]['daily_return']
    downside_std = downside_ret.std()
    sortino = (mean_ret - Rf_daily) / downside_std * np.sqrt(252) if downside_std > 0 else 0
    
    g_bench = group.dropna(subset=['bench_return'])
    if len(g_bench) > 10:
        slope, intercept, r_val, p_val, std_err = linregress(g_bench['bench_return'], g_bench['daily_return'])
        alpha = intercept * 252
        beta = slope
    else:
        alpha, beta = np.nan, np.nan
        
    running_max = group['nav'].cummax()
    drawdown = group['nav'] / running_max - 1
    max_dd = drawdown.min()
    
    results.append({
        'amfi_code': code,
        'cagr_1y': cagr_1y,
        'cagr_3y': cagr_3y,
        'cagr_5y': cagr_5y,
        'sharpe': sharpe,
        'sortino': sortino,
        'alpha': alpha,
        'beta': beta,
        'max_dd': max_dd
    })

df_res = pd.DataFrame(results)
df_res = df_res.merge(df_fund[['amfi_code', 'scheme_name', 'expense_ratio_pct']], on='amfi_code')

# Ranks
df_res['cagr_3y_rank'] = df_res['cagr_3y'].rank(ascending=True)
df_res['sharpe_rank'] = df_res['sharpe'].rank(ascending=True)
df_res['alpha_rank'] = df_res['alpha'].rank(ascending=True)
df_res['exp_rank'] = df_res['expense_ratio_pct'].rank(ascending=False)
df_res['dd_rank'] = df_res['max_dd'].rank(ascending=True)

df_res['composite_score'] = (
    0.30 * df_res['cagr_3y_rank'].fillna(0) + 
    0.25 * df_res['sharpe_rank'].fillna(0) +
    0.20 * df_res['alpha_rank'].fillna(0) +
    0.15 * df_res['exp_rank'].fillna(0) +
    0.10 * df_res['dd_rank'].fillna(0)
)
df_res['scorecard_0_100'] = (df_res['composite_score'] - df_res['composite_score'].min()) / (df_res['composite_score'].max() - df_res['composite_score'].min()) * 100

print("Saving CSVs...")
df_res.to_csv(f'{processed_dir}/fund_scorecard.csv', index=False)
df_res[['amfi_code', 'scheme_name', 'alpha', 'beta']].to_csv(f'{processed_dir}/alpha_beta.csv', index=False)

print("Plotting Benchmark Comparison...")
top_5 = df_res.sort_values('scorecard_0_100', ascending=False).head(5)
plt.figure(figsize=(12, 6))

min_date = df_nav['date'].max() - pd.DateOffset(years=3)
df_chart = df_nav[(df_nav['amfi_code'].isin(top_5['amfi_code'])) & (df_nav['date'] >= min_date)]

te_results = []

for code in top_5['amfi_code']:
    d = df_chart[df_chart['amfi_code'] == code].sort_values('date')
    if len(d) > 0:
        d['nav_rebased'] = d['nav'] / d['nav'].iloc[0] * 100
        name = top_5[top_5['amfi_code'] == code]['scheme_name'].values[0]
        plt.plot(d['date'], d['nav_rebased'], label=name)
        
        # Tracking Error vs Nifty 100
        d_te = d.dropna(subset=['daily_return', 'bench_return'])
        te = (d_te['daily_return'] - d_te['bench_return']).std() * np.sqrt(252)
        te_results.append({'scheme': name, 'tracking_error': te})
    
d_b100 = df_bench_100[df_bench_100['date'] >= min_date].sort_values('date')
if len(d_b100) > 0:
    d_b100['close_rebased'] = d_b100['close_value'] / d_b100['close_value'].iloc[0] * 100
    plt.plot(d_b100['date'], d_b100['close_rebased'], label='NIFTY 100', linestyle='--', color='black', linewidth=2)

d_b50 = df_bench_50[df_bench_50['date'] >= min_date].sort_values('date')
if len(d_b50) > 0:
    d_b50['close_rebased'] = d_b50['close_value'] / d_b50['close_value'].iloc[0] * 100
    plt.plot(d_b50['date'], d_b50['close_rebased'], label='NIFTY 50', linestyle=':', color='gray', linewidth=2)

plt.title('Top 5 Funds vs Benchmarks (3-Year Rebased to 100)')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig(f'{charts_dir}/benchmark_comparison_chart.png')

print("Tracking Errors for Top 5 Funds vs Nifty 100:")
for item in te_results:
    print(f"- {item['scheme']}: {item['tracking_error']:.4f}")

print("Generating Notebook...")
nb = nbf.v4.new_notebook()
def add_md(t): nb.cells.append(nbf.v4.new_markdown_cell(t))
def add_code(c): nb.cells.append(nbf.v4.new_code_cell(c))

add_md("# Fund Performance Analytics")
add_code(f'''
import pandas as pd
df_scorecard = pd.read_csv("../data/processed/fund_scorecard.csv")
df_alpha = pd.read_csv("../data/processed/alpha_beta.csv")
print("Top 5 Funds by Scorecard:")
display(df_scorecard.sort_values("scorecard_0_100", ascending=False).head()[['scheme_name', 'scorecard_0_100', 'cagr_3y', 'sharpe']])
''')

te_md = "## Tracking Error for Top 5 Funds vs Nifty 100\n"
for item in te_results:
    te_md += f"- **{item['scheme']}**: {item['tracking_error']:.4f}\n"
add_md(te_md)

add_md("## Benchmark Comparison Chart")
add_code('''
from IPython.display import Image
display(Image(filename="../reports/charts/benchmark_comparison_chart.png"))
''')

with open('../notebooks/04_performance_analytics.ipynb', 'w', encoding='utf-8') as f:
    nbf.write(nb, f)

print("Task 4 completed.")
