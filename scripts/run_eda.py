"""
run_eda.py
Generates all EDA charts from cleaned CSVs and saves them to reports/charts/.
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # non-interactive backend - prevents GUI popup
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import os
import warnings
from pathlib import Path

warnings.filterwarnings('ignore')

BASE_DIR      = Path(__file__).parent.parent
processed_dir = BASE_DIR / 'data' / 'processed'
charts_dir    = BASE_DIR / 'reports' / 'charts'
charts_dir.mkdir(parents=True, exist_ok=True)

print("Loading datasets...")
df_nav   = pd.read_csv(processed_dir / '02_nav_history_clean.csv', parse_dates=['date'])
df_fund  = pd.read_csv(processed_dir / '01_fund_master_clean.csv')
df_aum   = pd.read_csv(processed_dir / '03_aum_by_fund_house_clean.csv')
df_sip   = pd.read_csv(processed_dir / '04_monthly_sip_inflows_clean.csv')
df_cat   = pd.read_csv(processed_dir / '05_category_inflows_clean.csv')
df_txn   = pd.read_csv(processed_dir / '08_investor_transactions_clean.csv')
df_folio = pd.read_csv(processed_dir / '06_industry_folio_count_clean.csv')
df_perf  = pd.read_csv(processed_dir / '07_scheme_performance_clean.csv')
df_port  = pd.read_csv(processed_dir / '09_portfolio_holdings_clean.csv')

# ── Chart 1: NAV Trend (Plotly) ────────────────────────────────────────────
print("Chart 1: NAV Trend...")
df_nav_full = df_nav.merge(df_fund[['amfi_code', 'scheme_name']], on='amfi_code')
fig = px.line(
    df_nav_full, x='date', y='nav', color='scheme_name',
    title='Daily NAV Trend for 40 Schemes (2022-2026)',
    labels={'nav': 'Net Asset Value (INR)', 'date': 'Date'}
)
fig.add_vrect(x0="2023-01-01", x1="2023-12-31", fillcolor="green",  opacity=0.08, line_width=0, annotation_text="2023 Bull Run")
fig.add_vrect(x0="2024-01-01", x1="2024-06-30", fillcolor="crimson", opacity=0.08, line_width=0, annotation_text="2024 Correction")
try:
    fig.write_image(str(charts_dir / 'nav_trend.png'), width=1200, height=600)
    print("  Saved nav_trend.png")
except Exception as e:
    print(f"  Could not save plotly image (kaleido): {e}")

# ── Chart 2: AUM Growth by Fund House ─────────────────────────────────────
print("Chart 2: AUM Growth...")
df_aum['year'] = pd.to_datetime(df_aum['date']).dt.year
aum_yearly = df_aum.groupby(['year', 'fund_house'])['aum_lakh_crore'].mean().reset_index()
aum_max    = aum_yearly['aum_lakh_crore'].max()
top_house  = aum_yearly.loc[aum_yearly['aum_lakh_crore'].idxmax(), 'fund_house']

fig2, ax2 = plt.subplots(figsize=(13, 6))
sns.barplot(data=aum_yearly, x='year', y='aum_lakh_crore', hue='fund_house', ax=ax2)
ax2.set_title('AUM Growth by Fund House (2022-2025)', fontsize=14, fontweight='bold')
ax2.set_ylabel('AUM (Lakh Crore INR)')
ax2.set_xlabel('Year')
# Annotation: use axis fraction co-ordinates to avoid coordinate mismatch
ax2.annotate(
    f'{top_house} ({aum_max:.1f}L Cr)',
    xy=(0.85, 0.92), xycoords='axes fraction',
    fontsize=9, color='darkred',
    bbox=dict(boxstyle='round,pad=0.3', facecolor='lightyellow', alpha=0.8)
)
ax2.legend(bbox_to_anchor=(1.01, 1), loc='upper left', fontsize=8)
plt.tight_layout()
plt.savefig(charts_dir / 'aum_growth.png', bbox_inches='tight')
plt.close(fig2)

# ── Chart 3: Monthly SIP Inflow Trend (Plotly) ────────────────────────────
print("Chart 3: SIP Inflow...")
df_sip['date'] = pd.to_datetime(df_sip['month'])
sip_max     = df_sip['sip_inflow_crore'].max()
sip_max_dt  = df_sip.loc[df_sip['sip_inflow_crore'].idxmax(), 'date']
fig3 = px.line(
    df_sip, x='date', y='sip_inflow_crore',
    title='Monthly SIP Inflows (Jan 2022 - Dec 2025)',
    markers=True,
    labels={'sip_inflow_crore': 'SIP Inflow (Crore)', 'date': 'Month'}
)
fig3.add_annotation(
    x=str(sip_max_dt)[:10], y=sip_max,
    text=f"ATH: {sip_max:,.0f} Cr",
    showarrow=True, arrowhead=2, bgcolor='white', bordercolor='red'
)
try:
    fig3.write_image(str(charts_dir / 'sip_inflow_trend.png'), width=1000, height=500)
    print("  Saved sip_inflow_trend.png")
except Exception as e:
    print(f"  Could not save: {e}")

# ── Chart 4: Category Inflow Heatmap ──────────────────────────────────────
print("Chart 4: Category Heatmap...")
df_cat['month_dt'] = pd.to_datetime(df_cat['month'])
df_cat_sorted = df_cat.sort_values('month_dt')
pivot_cat = df_cat_sorted.pivot_table(
    index='category', columns='month', values='net_inflow_crore', aggfunc='sum'
)
# Sort columns chronologically
sorted_cols = [c for c in sorted(pivot_cat.columns, key=lambda x: pd.to_datetime(x))]
pivot_cat = pivot_cat[sorted_cols]

fig4, ax4 = plt.subplots(figsize=(14, 6))
sns.heatmap(pivot_cat, cmap='RdYlGn', center=0, annot=False, ax=ax4,
            cbar_kws={'label': 'Net Inflow (Cr)'})
ax4.set_title('Net Inflows by Fund Category (FY 24-25)', fontsize=14, fontweight='bold')
ax4.set_xlabel('Month')
ax4.set_ylabel('Category')
plt.xticks(rotation=45, ha='right', fontsize=7)
plt.tight_layout()
plt.savefig(charts_dir / 'category_heatmap.png', bbox_inches='tight')
plt.close(fig4)

# ── Chart 5: Investor Demographics ────────────────────────────────────────
print("Chart 5: Demographics...")
sip_txns = df_txn[df_txn['transaction_type'] == 'SIP'].copy()
age_order = ['18-25', '26-35', '36-45', '46-55', '56+']

fig5, axes5 = plt.subplots(1, 3, figsize=(18, 5))
fig5.suptitle('Investor Demographics', fontsize=15, fontweight='bold')

age_counts = df_txn['age_group'].value_counts().reindex(age_order).dropna()
axes5[0].pie(age_counts, labels=age_counts.index, autopct='%1.1f%%',
             colors=sns.color_palette('pastel'), startangle=140)
axes5[0].set_title('Age Group Distribution')

sns.boxplot(data=sip_txns, x='age_group', y='amount_inr', ax=axes5[1],
            order=age_order, palette='pastel')
axes5[1].set_title('SIP Amount by Age Group')
axes5[1].set_ylim(0, sip_txns['amount_inr'].quantile(0.95))
axes5[1].set_ylabel('SIP Amount (INR)')

gender_counts = df_txn['gender'].value_counts()
axes5[2].pie(gender_counts, labels=gender_counts.index, autopct='%1.1f%%',
             colors=['#66b3ff', '#ff9999'], startangle=140)
axes5[2].set_title('Gender Split')

plt.tight_layout()
plt.savefig(charts_dir / 'investor_demographics.png', bbox_inches='tight')
plt.close(fig5)

# ── Chart 6: Geographic Distribution ──────────────────────────────────────
print("Chart 6: Geographic...")
fig6, axes6 = plt.subplots(1, 2, figsize=(16, 6))
fig6.suptitle('Geographic Distribution of SIP Investments', fontsize=14, fontweight='bold')

state_sip = sip_txns.groupby('state')['amount_inr'].sum().sort_values(ascending=True)
state_sip.plot(kind='barh', ax=axes6[0], color='steelblue')
axes6[0].set_title('Total SIP Amount by State')
axes6[0].set_xlabel('Total Amount (INR)')

tier_counts = df_txn['city_tier'].value_counts()
axes6[1].pie(tier_counts, labels=tier_counts.index, autopct='%1.1f%%',
             colors=['#99ff99', '#ffcc99'], startangle=140)
axes6[1].set_title('City Tier (T30 vs B30)')

plt.tight_layout()
plt.savefig(charts_dir / 'geographic_dist.png', bbox_inches='tight')
plt.close(fig6)

# ── Chart 7: Folio Growth (Plotly) ────────────────────────────────────────
print("Chart 7: Folio Growth...")
df_folio['date'] = pd.to_datetime(df_folio['month'])
folio_min   = df_folio['total_folios_crore'].min()
folio_max   = df_folio['total_folios_crore'].max()
folio_start = str(df_folio.loc[df_folio['total_folios_crore'].idxmin(), 'date'])[:10]
folio_end   = str(df_folio.loc[df_folio['total_folios_crore'].idxmax(), 'date'])[:10]

fig7 = px.line(df_folio, x='date', y='total_folios_crore',
               title='Mutual Fund Industry Folio Growth (2022-2025)',
               markers=True,
               labels={'total_folios_crore': 'Total Folios (Crore)', 'date': 'Month'})
fig7.add_annotation(x=folio_start, y=folio_min,
                    text=f"{folio_min:.2f} Cr", showarrow=True, arrowhead=2)
fig7.add_annotation(x=folio_end,   y=folio_max,
                    text=f"{folio_max:.2f} Cr", showarrow=True, arrowhead=2)
try:
    fig7.write_image(str(charts_dir / 'folio_growth.png'), width=1000, height=500)
    print("  Saved folio_growth.png")
except Exception as e:
    print(f"  Could not save: {e}")

# ── Chart 8: NAV Return Correlation Matrix ────────────────────────────────
print("Chart 8: Correlation Matrix...")
top_10_codes = df_fund['amfi_code'].head(10).tolist()
df_nav_10    = df_nav_full[df_nav_full['amfi_code'].isin(top_10_codes)].copy()
df_nav_10    = df_nav_10.sort_values(['scheme_name', 'date'])
df_nav_10['daily_return'] = df_nav_10.groupby('scheme_name')['nav'].pct_change()

pivot_ret = (
    df_nav_10.pivot_table(index='date', columns='scheme_name', values='daily_return')
             .dropna()
)
corr_matrix = pivot_ret.corr()

# Shorten labels for readability
short_labels = {name: name.split(' - ')[0][:20] for name in corr_matrix.columns}
corr_matrix  = corr_matrix.rename(columns=short_labels, index=short_labels)

fig8, ax8 = plt.subplots(figsize=(12, 9))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', vmin=0.5, vmax=1.0,
            fmt='.2f', ax=ax8, annot_kws={'size': 8})
ax8.set_title('Daily Return Correlation Matrix (Top 10 Funds)', fontsize=13, fontweight='bold')
plt.xticks(rotation=30, ha='right', fontsize=8)
plt.yticks(rotation=0, fontsize=8)
plt.tight_layout()
plt.savefig(charts_dir / 'nav_correlation.png', bbox_inches='tight')
plt.close(fig8)

# ── Chart 9: Sector Allocation Donut ──────────────────────────────────────
print("Chart 9: Sector Donut...")
sector_weights = df_port.groupby('sector')['market_value_cr'].sum().sort_values(ascending=False)
threshold      = sector_weights.sum() * 0.04   # group <4% into Others
small_sectors  = sector_weights[sector_weights < threshold].sum()
sector_weights = sector_weights[sector_weights >= threshold].copy()
if small_sectors > 0:
    sector_weights['Others'] = small_sectors

fig9, ax9 = plt.subplots(figsize=(9, 9))
wedges, texts, autotexts = ax9.pie(
    sector_weights, labels=sector_weights.index,
    autopct='%1.1f%%', pctdistance=0.82,
    colors=sns.color_palette('tab20', len(sector_weights)),
    startangle=140, wedgeprops=dict(width=0.55)
)
for t in autotexts:
    t.set_fontsize(8)
ax9.set_title('Aggregate Sector Allocation (Equity Funds)', fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig(charts_dir / 'sector_allocation.png', bbox_inches='tight')
plt.close(fig9)

# ── Chart 10: Expense Ratio Distribution ──────────────────────────────────
print("Chart 10: Expense Ratio...")
fig10, ax10 = plt.subplots(figsize=(10, 5))
sns.histplot(df_fund['expense_ratio_pct'].dropna(), bins=12, kde=True,
             color='slateblue', ax=ax10)
ax10.set_title('Distribution of Fund Expense Ratios', fontsize=13, fontweight='bold')
ax10.set_xlabel('Expense Ratio (%)')
ax10.set_ylabel('Count')
ax10.axvline(df_fund['expense_ratio_pct'].mean(), color='red', linestyle='--',
             label=f"Mean: {df_fund['expense_ratio_pct'].mean():.2f}%")
ax10.legend()
plt.tight_layout()
plt.savefig(charts_dir / 'expense_ratio_dist.png', bbox_inches='tight')
plt.close(fig10)

# ── Chart 11: AUM by Category ─────────────────────────────────────────────
print("Chart 11: AUM by Category...")
cat_aum = df_perf.groupby('category')['aum_crore'].sum().sort_values(ascending=False)
fig11, ax11 = plt.subplots(figsize=(8, 6))
cat_aum.plot(kind='bar', color=sns.color_palette('Set2', len(cat_aum)), ax=ax11)
ax11.set_title('Total AUM by Fund Category', fontsize=13, fontweight='bold')
ax11.set_ylabel('AUM (Crore INR)')
ax11.set_xlabel('Category')
plt.xticks(rotation=20, ha='right')
plt.tight_layout()
plt.savefig(charts_dir / 'aum_by_category.png', bbox_inches='tight')
plt.close(fig11)

# ── Chart 12: Risk vs Return Scatter ──────────────────────────────────────
print("Chart 12: Risk-Return Scatter...")
df_valid = df_perf.dropna(subset=['std_dev_ann_pct', 'return_3yr_pct', 'aum_crore'])
fig12, ax12 = plt.subplots(figsize=(11, 7))
scatter = ax12.scatter(
    df_valid['std_dev_ann_pct'], df_valid['return_3yr_pct'],
    s=df_valid['aum_crore'] / df_valid['aum_crore'].max() * 600 + 30,
    c=df_valid['sharpe_ratio'], cmap='RdYlGn', alpha=0.8, edgecolors='grey', linewidths=0.5
)
plt.colorbar(scatter, ax=ax12, label='Sharpe Ratio')
ax12.set_title('Risk vs 3-Year Return (Bubble Size = AUM)', fontsize=13, fontweight='bold')
ax12.set_xlabel('Annualised Std Dev (%)')
ax12.set_ylabel('3-Year Return (%)')
ax12.axhline(0, color='grey', linewidth=0.8, linestyle='--')
plt.tight_layout()
plt.savefig(charts_dir / 'risk_return_scatter.png', bbox_inches='tight')
plt.close(fig12)

print("All 12 charts generated and saved successfully.")
