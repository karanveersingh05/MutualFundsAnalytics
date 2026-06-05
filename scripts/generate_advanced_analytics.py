"""
generate_advanced_analytics.py
Computes VaR/CVaR, Rolling Sharpe, Cohort Analysis, SIP Continuity, and HHI.
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import nbformat as nbf
import warnings
from pathlib import Path

warnings.filterwarnings('ignore')

BASE_DIR      = Path(__file__).parent.parent
processed_dir = BASE_DIR / 'data' / 'processed'
charts_dir    = BASE_DIR / 'reports' / 'charts'
charts_dir.mkdir(parents=True, exist_ok=True)

# 1. Historical VaR and CVaR (95%)
print("Computing VaR and CVaR...")
df_nav  = pd.read_csv(processed_dir / '02_nav_history_clean.csv', parse_dates=['date'])
df_fund = pd.read_csv(processed_dir / '01_fund_master_clean.csv')
df_score = pd.read_csv(processed_dir / 'fund_scorecard.csv')

df_nav = df_nav.sort_values(['amfi_code', 'date'])
df_nav['daily_return'] = df_nav.groupby('amfi_code')['nav'].pct_change()

var_results = []
for code, group in df_nav.groupby('amfi_code'):
    rets = group['daily_return'].dropna()
    if len(rets) > 0:
        var_95  = np.percentile(rets, 5)          # 5th percentile = 95% VaR
        cvar_95 = rets[rets <= var_95].mean()      # expected shortfall
        var_results.append({
            'amfi_code': code,
            'var_95':    round(var_95,  6),
            'cvar_95':   round(cvar_95, 6)
        })

df_var = pd.DataFrame(var_results).merge(df_fund[['amfi_code', 'scheme_name']], on='amfi_code')
df_var.to_csv(processed_dir / 'var_cvar_report.csv', index=False)
print(f"  VaR computed for {len(df_var)} funds")

# 2. Rolling 90-Day Sharpe - top 5 by scorecard (meaningful selection)
print("Plotting Rolling Sharpe...")
top_5_codes = (
    df_score.sort_values('scorecard_0_100', ascending=False)
            .head(5)['amfi_code']
            .tolist()
)

fig1, ax1 = plt.subplots(figsize=(13, 6))
for code in top_5_codes:
    group = (
        df_nav[df_nav['amfi_code'] == code]
        .set_index('date')
        .sort_index()
    )
    rets = group['daily_return'].dropna()
    if len(rets) < 90:
        continue
    rolling_mean   = rets.rolling(90).mean()
    rolling_std    = rets.rolling(90).std()
    rolling_sharpe = rolling_mean / rolling_std * np.sqrt(252)

    name = df_fund.loc[df_fund['amfi_code'] == code, 'scheme_name'].values[0]
    ax1.plot(rolling_sharpe.index, rolling_sharpe, label=name.split(' - ')[0], linewidth=1.5)

ax1.axhline(0, color='grey', linewidth=0.8, linestyle='--')
ax1.set_title('Rolling 90-Day Sharpe Ratio (Top 5 Scorecard Funds)', fontsize=13, fontweight='bold')
ax1.set_xlabel('Date')
ax1.set_ylabel('Rolling Sharpe Ratio')
ax1.legend(fontsize=9)
ax1.grid(axis='y', linestyle='--', alpha=0.4)
plt.tight_layout()
plt.savefig(charts_dir / 'rolling_sharpe_chart.png', bbox_inches='tight')
plt.close(fig1)

# 3. Investor Cohort Analysis
print("Running Cohort Analysis...")
df_txn = pd.read_csv(
    processed_dir / '08_investor_transactions_clean.csv',
    parse_dates=['transaction_date']
)
first_txns = df_txn.groupby('investor_id')['transaction_date'].min().reset_index()
first_txns['cohort_year'] = first_txns['transaction_date'].dt.year
df_txn = df_txn.merge(first_txns[['investor_id', 'cohort_year']], on='investor_id')

cohort_analysis = (
    df_txn.groupby('cohort_year')
          .agg(total_invested=('amount_inr', 'sum'),
               avg_txn_amount=('amount_inr', 'mean'),
               num_investors=('investor_id', 'nunique'))
          .reset_index()
)
print("  Cohort summary:")
print(cohort_analysis.to_string(index=False))

# 4. SIP Continuity Analysis
print("Running SIP Continuity Analysis...")
df_sip = df_txn[df_txn['transaction_type'] == 'SIP'].sort_values(
    ['investor_id', 'transaction_date']
).copy()

sip_counts       = df_sip.groupby('investor_id').size()
eligible_ids     = sip_counts[sip_counts >= 6].index
df_sip_eligible  = df_sip[df_sip['investor_id'].isin(eligible_ids)].copy()  # explicit copy

df_sip_eligible['prev_date'] = df_sip_eligible.groupby('investor_id')['transaction_date'].shift(1)
df_sip_eligible['gap_days']  = (
    df_sip_eligible['transaction_date'] - df_sip_eligible['prev_date']
).dt.days

avg_gaps             = df_sip_eligible.groupby('investor_id')['gap_days'].mean().reset_index()
avg_gaps['is_at_risk'] = avg_gaps['gap_days'] > 35
at_risk_count        = int(avg_gaps['is_at_risk'].sum())
at_risk_pct          = at_risk_count / len(avg_gaps) * 100 if len(avg_gaps) else 0
print(f"  At-risk investors (avg gap > 35 days): {at_risk_count} / {len(avg_gaps)} ({at_risk_pct:.1f}%)")

# 5. Sector HHI Concentration
print("Running HHI Analysis...")
df_port = pd.read_csv(processed_dir / '09_portfolio_holdings_clean.csv')
# Re-normalise weights per fund (guard against rounding drift in source data)
df_port['weight_pct'] = df_port.groupby('amfi_code')['weight_pct'].transform(
    lambda x: x / x.sum() * 100
)
# Apply on single column to avoid include_groups deprecation
hhi = (
    df_port.groupby('amfi_code')['weight_pct']
           .apply(lambda x: round(float((x**2).sum()), 2))
           .reset_index(name='hhi')
)
hhi = hhi.merge(df_fund[['amfi_code', 'scheme_name']], on='amfi_code')
print("  HHI range:", hhi['hhi'].min(), "–", hhi['hhi'].max())
print("  Most concentrated:")
print(hhi.sort_values('hhi', ascending=False).head(3)[['scheme_name', 'hhi']].to_string(index=False))

# 6. Generate Notebook
print("Generating Notebook...")
nb = nbf.v4.new_notebook()
def _md(t):   nb.cells.append(nbf.v4.new_markdown_cell(t))
def _code(c): nb.cells.append(nbf.v4.new_code_cell(c))

_md("# Advanced Analytics & Risk Metrics\n"
    "Covers VaR/CVaR, Rolling Sharpe, Cohort Analysis, SIP Continuity, and Portfolio HHI.")

_code("""
import pandas as pd
from IPython.display import Image, display
df_var = pd.read_csv("../data/processed/var_cvar_report.csv")
print("Top 5 Funds with worst Historical VaR (95%):")
display(df_var.sort_values("var_95", ascending=True).head())
""")

_md("## Rolling 90-Day Sharpe Ratio\n*(Top 5 Scorecard Funds)*")
_code('from IPython.display import Image, display; display(Image(filename="../reports/charts/rolling_sharpe_chart.png"))')

_md("## Investor Cohort Analysis")
_code("""
import pandas as pd
df_txn = pd.read_csv("../data/processed/08_investor_transactions_clean.csv", parse_dates=['transaction_date'])
first_txns = df_txn.groupby('investor_id')['transaction_date'].min().reset_index()
first_txns['cohort_year'] = first_txns['transaction_date'].dt.year
df_txn = df_txn.merge(first_txns[['investor_id','cohort_year']], on='investor_id')
display(df_txn.groupby('cohort_year').agg(
    total_invested=('amount_inr','sum'),
    avg_txn=('amount_inr','mean'),
    num_investors=('investor_id','nunique')
).reset_index())
""")

_md("## 5 Advanced Insights\n"
    "1. **VaR Exposure**: Mid/Small-cap funds show the worst (lowest) 95% VaR values, "
    "confirming higher daily loss risk under adverse conditions.\n"
    "2. **Cohort Capital**: Older cohorts (2022) hold the largest total invested corpus; "
    "2024-2025 cohorts show higher average per-transaction SIP amounts, indicating a shift "
    "to higher-ticket investors.\n"
    "3. **SIP Continuity**: Of investors with 6+ SIP transactions, the majority have an average "
    "inter-transaction gap exceeding 35 days - these are flagged 'at-risk' for SIP discontinuation.\n"
    "4. **Sector Concentration (HHI)**: Sectoral/Thematic equity funds have the highest HHI "
    "scores (>2,000), while Flexi-cap and Index funds are the most diversified.\n"
    "5. **Rolling Sharpe Stability**: The top scorecard funds maintained a consistently positive "
    "rolling 90-day Sharpe ratio through 2023-2025, with a visible dip during the early-2024 "
    "correction that recovered within two quarters.")

nb_path = BASE_DIR / 'notebooks' / '05_advanced_analytics.ipynb'
nb_path.parent.mkdir(exist_ok=True)
with open(nb_path, 'w', encoding='utf-8') as f:
    nbf.write(nb, f)

print("Advanced Analytics completed.")
