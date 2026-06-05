"""
compute_metrics.py
Computes fund performance metrics: CAGR, Sharpe, Sortino, Alpha, Beta, Max DD.
Produces fund_scorecard.csv, alpha_beta.csv, and benchmark comparison chart.
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.stats import linregress
import nbformat as nbf
import warnings
from pathlib import Path

warnings.filterwarnings('ignore')

BASE_DIR      = Path(__file__).parent.parent
processed_dir = BASE_DIR / 'data' / 'processed'
charts_dir    = BASE_DIR / 'reports' / 'charts'
charts_dir.mkdir(parents=True, exist_ok=True)

print("Loading data...")
df_nav  = pd.read_csv(processed_dir / '02_nav_history_clean.csv', parse_dates=['date'])
df_fund = pd.read_csv(processed_dir / '01_fund_master_clean.csv')
df_bench = pd.read_csv(processed_dir / '10_benchmark_indices_clean.csv', parse_dates=['date'])

# Daily returns
print("Computing metrics...")
df_nav = df_nav.sort_values(['amfi_code', 'date'])
df_nav['daily_return'] = df_nav.groupby('amfi_code')['nav'].pct_change()

# Benchmark returns
df_bench_100 = df_bench[df_bench['index_name'] == 'NIFTY100'].sort_values('date').copy()
df_bench_100['bench_return'] = df_bench_100['close_value'].pct_change()

df_bench_50 = df_bench[df_bench['index_name'] == 'NIFTY50'].sort_values('date').copy()
df_bench_50['bench_return_50'] = df_bench_50['close_value'].pct_change()

df_nav = df_nav.merge(df_bench_100[['date', 'bench_return']], on='date', how='left')
df_nav = df_nav.merge(df_bench_50[['date', 'bench_return_50']], on='date', how='left')

results = []
Rf       = 0.065          # RBI repo rate proxy
Rf_daily = Rf / 252

for code, group in df_nav.groupby('amfi_code'):
    group = group.dropna(subset=['daily_return']).copy()
    if len(group) < 30:
        continue

    end_val   = group['nav'].iloc[-1]

    # CAGR — calendar-day based for accuracy
    total_days = (group['date'].iloc[-1] - group['date'].iloc[0]).days

    cagr_1y = cagr_3y = cagr_5y = np.nan
    if total_days >= 365:
        v = group[group['date'] <= group['date'].iloc[-1] - pd.DateOffset(years=1)]['nav']
        if len(v):
            cagr_1y = (end_val / v.iloc[-1]) - 1
    if total_days >= 365 * 3:
        v = group[group['date'] <= group['date'].iloc[-1] - pd.DateOffset(years=3)]['nav']
        if len(v):
            cagr_3y = (end_val / v.iloc[-1]) ** (1/3) - 1
    if total_days >= 365 * 5:
        v = group[group['date'] <= group['date'].iloc[-1] - pd.DateOffset(years=5)]['nav']
        if len(v):
            cagr_5y = (end_val / v.iloc[-1]) ** (1/5) - 1

    # Sharpe
    mean_ret = group['daily_return'].mean()
    std_ret  = group['daily_return'].std()
    sharpe   = (mean_ret - Rf_daily) / std_ret * np.sqrt(252) if std_ret > 0 else 0.0

    # Sortino — downside std only
    neg_rets     = group[group['daily_return'] < 0]['daily_return']
    downside_std = neg_rets.std()
    sortino      = (mean_ret - Rf_daily) / downside_std * np.sqrt(252) if downside_std > 0 else 0.0

    # Alpha & Beta (OLS on Nifty 100)
    g_bench = group.dropna(subset=['bench_return'])
    if len(g_bench) > 10:
        slope, intercept, *_ = linregress(g_bench['bench_return'], g_bench['daily_return'])
        alpha = intercept * 252   # annualised
        beta  = slope
    else:
        alpha = beta = np.nan

    # Maximum Drawdown
    running_max = group['nav'].cummax()
    drawdown    = group['nav'] / running_max - 1
    max_dd      = drawdown.min()

    results.append({
        'amfi_code': code,
        'cagr_1y':  round(cagr_1y, 6)  if pd.notna(cagr_1y)  else np.nan,
        'cagr_3y':  round(cagr_3y, 6)  if pd.notna(cagr_3y)  else np.nan,
        'cagr_5y':  round(cagr_5y, 6)  if pd.notna(cagr_5y)  else np.nan,
        'sharpe':   round(sharpe,  4),
        'sortino':  round(sortino, 4),
        'alpha':    round(alpha,   6)   if pd.notna(alpha)     else np.nan,
        'beta':     round(beta,    4)   if pd.notna(beta)      else np.nan,
        'max_dd':   round(max_dd,  6),
    })

df_res = pd.DataFrame(results)
df_res = df_res.merge(df_fund[['amfi_code', 'scheme_name', 'expense_ratio_pct']], on='amfi_code')

# Fund Scorecard: higher rank = better
# cagr_3y, sharpe, alpha   → ascending=True  → higher value = higher rank (correct)
# expense_ratio_pct         → ascending=False → lower expense = higher rank
# max_dd                    → ascending=True  → less negative = higher rank (closer to 0 = better)
df_res['cagr_3y_rank'] = df_res['cagr_3y'].rank(ascending=True, na_option='bottom')
df_res['sharpe_rank']  = df_res['sharpe'].rank(ascending=True,  na_option='bottom')
df_res['alpha_rank']   = df_res['alpha'].rank(ascending=True,   na_option='bottom')
df_res['exp_rank']     = df_res['expense_ratio_pct'].rank(ascending=False, na_option='bottom')
df_res['dd_rank']      = df_res['max_dd'].rank(ascending=False,  na_option='bottom')

df_res['composite_score'] = (
    0.30 * df_res['cagr_3y_rank'] +
    0.25 * df_res['sharpe_rank']  +
    0.20 * df_res['alpha_rank']   +
    0.15 * df_res['exp_rank']     +
    0.10 * df_res['dd_rank']
)
score_min = df_res['composite_score'].min()
score_max = df_res['composite_score'].max()
df_res['scorecard_0_100'] = (
    (df_res['composite_score'] - score_min) / (score_max - score_min) * 100
).round(2)

print("Saving CSVs...")
df_res.to_csv(processed_dir / 'fund_scorecard.csv', index=False)
df_res[['amfi_code', 'scheme_name', 'alpha', 'beta']].to_csv(
    processed_dir / 'alpha_beta.csv', index=False
)

# ── Benchmark Comparison Chart ─────────────────────────────────────────────
print("Plotting Benchmark Comparison...")
top_5   = df_res.sort_values('scorecard_0_100', ascending=False).head(5)
min_date = df_nav['date'].max() - pd.DateOffset(years=3)

fig, ax = plt.subplots(figsize=(13, 7))
te_results = []

for code in top_5['amfi_code']:
    d = df_nav[(df_nav['amfi_code'] == code) & (df_nav['date'] >= min_date)].sort_values('date')
    if len(d) == 0:
        continue
    d = d.copy()
    d['nav_rebased'] = d['nav'] / d['nav'].iloc[0] * 100
    name = top_5.loc[top_5['amfi_code'] == code, 'scheme_name'].values[0]
    short_name = name.split(' - ')[0]
    ax.plot(d['date'], d['nav_rebased'], label=short_name, linewidth=1.6)

    d_te = d.dropna(subset=['daily_return', 'bench_return'])
    if len(d_te) > 5:
        te = (d_te['daily_return'] - d_te['bench_return']).std() * np.sqrt(252)
        te_results.append({'scheme': short_name, 'tracking_error': round(te, 4)})

d_b100 = df_bench_100[df_bench_100['date'] >= min_date].sort_values('date')
if len(d_b100):
    d_b100 = d_b100.copy()
    d_b100['close_rebased'] = d_b100['close_value'] / d_b100['close_value'].iloc[0] * 100
    ax.plot(d_b100['date'], d_b100['close_rebased'],
            label='NIFTY 100', linestyle='--', color='black', linewidth=2.2)

d_b50 = df_bench_50[df_bench_50['date'] >= min_date].sort_values('date')
if len(d_b50):
    d_b50 = d_b50.copy()
    d_b50['close_rebased'] = d_b50['close_value'] / d_b50['close_value'].iloc[0] * 100
    ax.plot(d_b50['date'], d_b50['close_rebased'],
            label='NIFTY 50', linestyle=':', color='dimgray', linewidth=2.0)

ax.set_title('Top 5 Funds vs Benchmarks — 3-Year Performance (Rebased to 100)',
             fontsize=13, fontweight='bold')
ax.set_ylabel('Rebased NAV / Index (Base = 100)')
ax.set_xlabel('Date')
ax.legend(bbox_to_anchor=(1.01, 1), loc='upper left', fontsize=9)
ax.grid(axis='y', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig(charts_dir / 'benchmark_comparison_chart.png', bbox_inches='tight')
plt.close(fig)

print("Tracking Errors vs Nifty 100:")
for item in te_results:
    print(f"  {item['scheme']}: {item['tracking_error']:.4f}")

# ── Generate Notebook ──────────────────────────────────────────────────────
print("Generating Notebook...")
nb = nbf.v4.new_notebook()
def _md(t):  nb.cells.append(nbf.v4.new_markdown_cell(t))
def _code(c): nb.cells.append(nbf.v4.new_code_cell(c))

_md("# Fund Performance Analytics\nComputed metrics: CAGR (1/3/5yr), Sharpe, Sortino, Alpha, Beta, Max Drawdown, Scorecard.")

_code("""
import pandas as pd
df_scorecard = pd.read_csv("../data/processed/fund_scorecard.csv")
df_alpha     = pd.read_csv("../data/processed/alpha_beta.csv")
print("Top 10 Funds by Scorecard:")
display(df_scorecard.sort_values("scorecard_0_100", ascending=False)
        .head(10)[['scheme_name','scorecard_0_100','cagr_3y','sharpe','alpha','max_dd']])
""")

te_md = "## Tracking Error (Active Risk vs Nifty 100)\n\n| Fund | Tracking Error |\n|---|---|\n"
for item in te_results:
    te_md += f"| {item['scheme']} | {item['tracking_error']:.4f} |\n"
_md(te_md)

_md("## Benchmark Comparison Chart\n*(Top 5 funds rebased to 100 vs Nifty 50 & 100)*")
_code('from IPython.display import Image; display(Image(filename="../reports/charts/benchmark_comparison_chart.png"))')

nb_path = BASE_DIR / 'notebooks' / '04_performance_analytics.ipynb'
nb_path.parent.mkdir(exist_ok=True)
with open(nb_path, 'w', encoding='utf-8') as f:
    nbf.write(nb, f)

print("Task 4 completed.")
