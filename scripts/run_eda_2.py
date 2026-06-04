import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import warnings
warnings.filterwarnings('ignore')

processed_dir = 'data/processed'

df_fund = pd.read_csv(f'{processed_dir}/01_fund_master_clean.csv')
df_perf = pd.read_csv(f'{processed_dir}/07_scheme_performance_clean.csv')

plt.figure(figsize=(10, 5))
sns.histplot(df_fund['expense_ratio_pct'].dropna(), bins=10, kde=True, color='purple')
plt.title('Distribution of Expense Ratios')
plt.xlabel('Expense Ratio (%)')
plt.tight_layout()
plt.savefig('reports/charts/expense_ratio_dist.png')

plt.figure(figsize=(8, 8))
cat_aum = df_perf.groupby('category')['aum_crore'].sum()
plt.pie(cat_aum, labels=cat_aum.index, autopct='%1.1f%%', colors=sns.color_palette('Set2'))
plt.title('AUM Distribution by Category')
plt.tight_layout()
plt.savefig('reports/charts/aum_by_category.png')

plt.figure(figsize=(10, 6))
sns.scatterplot(data=df_perf, x='std_dev_ann_pct', y='return_3yr_pct', hue='category', size='aum_crore', sizes=(50, 500))
plt.title('Risk vs Return (3-Year)')
plt.xlabel('Annualized Standard Deviation (%)')
plt.ylabel('3-Year Return (%)')
plt.tight_layout()
plt.savefig('reports/charts/risk_return_scatter.png')
