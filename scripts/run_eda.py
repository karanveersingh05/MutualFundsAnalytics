import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import os
import warnings
warnings.filterwarnings('ignore')

os.makedirs('reports/charts', exist_ok=True)
processed_dir = 'data/processed'

df_nav = pd.read_csv(f'{processed_dir}/02_nav_history_clean.csv', parse_dates=['date'])
df_fund = pd.read_csv(f'{processed_dir}/01_fund_master_clean.csv')
df_aum = pd.read_csv(f'{processed_dir}/03_aum_by_fund_house_clean.csv')
df_sip = pd.read_csv(f'{processed_dir}/04_monthly_sip_inflows_clean.csv')
df_cat = pd.read_csv(f'{processed_dir}/05_category_inflows_clean.csv')
df_txn = pd.read_csv(f'{processed_dir}/08_investor_transactions_clean.csv')
df_folio = pd.read_csv(f'{processed_dir}/06_industry_folio_count_clean.csv')
df_perf = pd.read_csv(f'{processed_dir}/07_scheme_performance_clean.csv')
df_port = pd.read_csv(f'{processed_dir}/09_portfolio_holdings_clean.csv')

df_nav_full = df_nav.merge(df_fund[['amfi_code', 'scheme_name']], on='amfi_code')
fig = px.line(df_nav_full, x='date', y='nav', color='scheme_name', 
              title='Daily NAV Trend for 40 Schemes (2022-2026)',
              labels={'nav': 'Net Asset Value (INR)', 'date': 'Date'})
fig.add_vrect(x0="2023-01-01", x1="2023-12-31", fillcolor="green", opacity=0.1, line_width=0, annotation_text="2023 Bull Run")
fig.add_vrect(x0="2024-01-01", x1="2024-06-30", fillcolor="red", opacity=0.1, line_width=0, annotation_text="2024 Correction")
try:
    fig.write_image('reports/charts/nav_trend.png', width=1200, height=600)
except Exception as e:
    print(f"Could not save plotly image: {e}")

plt.figure(figsize=(12, 6))
df_aum['year'] = pd.to_datetime(df_aum['date']).dt.year
aum_yearly = df_aum.groupby(['year', 'fund_house'])['aum_lakh_crore'].mean().reset_index()
sns.barplot(data=aum_yearly, x='year', y='aum_lakh_crore', hue='fund_house')
plt.title('AUM Growth by Fund House (2022-2025)')
plt.ylabel('AUM (Lakh Crore INR)')
plt.annotate('SBI Dominance (12.5L Cr)', xy=(3, 12.5), xytext=(2, 11), arrowprops=dict(facecolor='black', shrink=0.05))
plt.tight_layout()
plt.savefig('reports/charts/aum_growth.png')

df_sip['date'] = pd.to_datetime(df_sip['month'])
fig = px.line(df_sip, x='date', y='sip_inflow_crore', title='Monthly SIP Inflows (Jan 2022 - Dec 2025)', markers=True)
fig.add_annotation(x='2025-12-01', y=31002, text="31,002 Cr ATH (Dec 2025)", showarrow=True, arrowhead=1)
try:
    fig.write_image('reports/charts/sip_inflow_trend.png', width=1000, height=500)
except:
    pass

plt.figure(figsize=(12, 6))
pivot_cat = df_cat.pivot_table(index='category', columns='month', values='net_inflow_crore', aggfunc='sum')
sns.heatmap(pivot_cat, cmap='RdYlGn', center=0, annot=False)
plt.title('Net Inflows by Fund Category (FY 24-25)')
plt.tight_layout()
plt.savefig('reports/charts/category_heatmap.png')

fig, axes = plt.subplots(1, 3, figsize=(18, 5))
age_counts = df_txn['age_group'].value_counts()
axes[0].pie(age_counts, labels=age_counts.index, autopct='%1.1f%%', colors=sns.color_palette('pastel'))
axes[0].set_title('Age Group Distribution')

sip_txns = df_txn[df_txn['transaction_type'] == 'SIP']
sns.boxplot(data=sip_txns, x='age_group', y='amount_inr', ax=axes[1], order=['18-25', '26-35', '36-45', '46-55', '56+'])
axes[1].set_title('SIP Amount by Age Group')
axes[1].set_ylim(0, sip_txns['amount_inr'].quantile(0.95))

gender_counts = df_txn['gender'].value_counts()
axes[2].pie(gender_counts, labels=gender_counts.index, autopct='%1.1f%%', colors=['#ff9999','#66b3ff'])
axes[2].set_title('Gender Split')

plt.tight_layout()
plt.savefig('reports/charts/investor_demographics.png')

fig, axes = plt.subplots(1, 2, figsize=(16, 6))
state_sip = sip_txns.groupby('state')['amount_inr'].sum().sort_values(ascending=True)
state_sip.plot(kind='barh', ax=axes[0], color='skyblue')
axes[0].set_title('Total SIP Amount by State')

tier_counts = df_txn['city_tier'].value_counts()
axes[1].pie(tier_counts, labels=tier_counts.index, autopct='%1.1f%%', colors=['#99ff99','#ffcc99'])
axes[1].set_title('City Tier (T30 vs B30)')

plt.tight_layout()
plt.savefig('reports/charts/geographic_dist.png')

df_folio['date'] = pd.to_datetime(df_folio['month'])
fig = px.line(df_folio, x='date', y='total_folios_crore', title='Mutual Fund Industry Folio Growth', markers=True)
fig.add_annotation(x='2022-01-01', y=13.26, text="13.26 Cr (Jan 2022)", showarrow=True)
fig.add_annotation(x='2025-12-01', y=26.12, text="26.12 Cr (Dec 2025)", showarrow=True)
try:
    fig.write_image('reports/charts/folio_growth.png', width=1000, height=500)
except:
    pass

top_10_funds = df_fund['amfi_code'].head(10).tolist()
df_nav_10 = df_nav_full[df_nav_full['amfi_code'].isin(top_10_funds)].copy()
df_nav_10 = df_nav_10.sort_values(['scheme_name', 'date'])
df_nav_10['daily_return'] = df_nav_10.groupby('scheme_name')['nav'].pct_change()

pivot_ret = df_nav_10.pivot(index='date', columns='scheme_name', values='daily_return').dropna()
corr_matrix = pivot_ret.corr()

plt.figure(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', vmin=0.5, vmax=1.0, fmt=".2f")
plt.title('Daily Return Correlation Matrix (Top 10 Funds)')
plt.tight_layout()
plt.savefig('reports/charts/nav_correlation.png')

plt.figure(figsize=(8, 8))
sector_weights = df_port.groupby('sector')['market_value_cr'].sum()
threshold = sector_weights.sum() * 0.05
small_sectors = sector_weights[sector_weights < threshold].sum()
sector_weights = sector_weights[sector_weights >= threshold]
sector_weights['Others'] = small_sectors

plt.pie(sector_weights, labels=sector_weights.index, autopct='%1.1f%%', pctdistance=0.85, colors=sns.color_palette('Set3'))
centre_circle = plt.Circle((0,0), 0.70, fc='white')
fig = plt.gcf()
fig.gca().add_artist(centre_circle)
plt.title('Aggregate Sector Allocation (Equity Funds)')
plt.tight_layout()
plt.savefig('reports/charts/sector_allocation.png')
print("All charts generated and saved successfully.")
