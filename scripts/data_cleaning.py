import pandas as pd
import numpy as np
import sqlite3
import os
from pathlib import Path

raw_dir = Path('../data/raw')
processed_dir = Path('../data/processed')
db_dir = Path('../data/db')

processed_dir.mkdir(parents=True, exist_ok=True)
db_dir.mkdir(parents=True, exist_ok=True)

# 1. Clean nav_history.csv
print("Cleaning nav_history.csv...")
df_nav = pd.read_csv(raw_dir / '02_nav_history.csv')
df_nav['date'] = pd.to_datetime(df_nav['date'])
df_nav = df_nav.sort_values(['amfi_code', 'date'])
df_nav = df_nav.drop_duplicates(subset=['amfi_code', 'date'])
df_nav = df_nav[df_nav['nav'] > 0]

min_date = df_nav['date'].min()
max_date = df_nav['date'].max()
all_dates = pd.date_range(start=min_date, end=max_date, freq='D')

def fill_missing_dates(group):
    group = group.set_index('date')
    group = group.reindex(all_dates)
    group['amfi_code'] = group['amfi_code'].ffill().bfill()
    group['nav'] = group['nav'].ffill()
    group = group.reset_index().rename(columns={'index': 'date'})
    return group

df_nav_clean = df_nav.groupby('amfi_code', group_keys=False).apply(fill_missing_dates)
df_nav_clean.to_csv(processed_dir / '02_nav_history_clean.csv', index=False)

# 2. Clean investor_transactions.csv
print("Cleaning investor_transactions.csv...")
df_txn = pd.read_csv(raw_dir / '08_investor_transactions.csv')
df_txn['transaction_type'] = df_txn['transaction_type'].str.strip().str.title()
df_txn['transaction_type'] = df_txn['transaction_type'].replace({'Sip': 'SIP'})
df_txn = df_txn[df_txn['amount_inr'] > 0]
df_txn['transaction_date'] = pd.to_datetime(df_txn['transaction_date']).dt.strftime('%Y-%m-%d')
df_txn['kyc_status'] = df_txn['kyc_status'].str.strip().str.title()
df_txn.to_csv(processed_dir / '08_investor_transactions_clean.csv', index=False)

# 3. Clean scheme_performance.csv
print("Cleaning scheme_performance.csv...")
df_perf = pd.read_csv(raw_dir / '07_scheme_performance.csv')
numeric_cols = ['return_1yr_pct', 'return_3yr_pct', 'return_5yr_pct', 'alpha', 'beta', 'sharpe_ratio', 'sortino_ratio']
for col in numeric_cols:
    df_perf[col] = pd.to_numeric(df_perf[col], errors='coerce')
df_perf.to_csv(processed_dir / '07_scheme_performance_clean.csv', index=False)

# Clean fund_master.csv
print("Cleaning 01_fund_master.csv...")
df_fund = pd.read_csv(raw_dir / '01_fund_master.csv')
df_fund['expense_ratio_pct'] = pd.to_numeric(df_fund['expense_ratio_pct'], errors='coerce')
df_fund['expense_ratio_pct'] = df_fund['expense_ratio_pct'].clip(lower=0.1, upper=2.5)
df_fund.to_csv(processed_dir / '01_fund_master_clean.csv', index=False)

# Process the rest
print("Copying remaining datasets to processed...")
rest_files = [
    '03_aum_by_fund_house.csv',
    '04_monthly_sip_inflows.csv',
    '05_category_inflows.csv',
    '06_industry_folio_count.csv',
    '09_portfolio_holdings.csv',
    '10_benchmark_indices.csv'
]
for f in rest_files:
    df = pd.read_csv(raw_dir / f)
    df.to_csv(processed_dir / f.replace('.csv', '_clean.csv'), index=False)

# Dim_date generation
print("Generating dim_date...")
dim_date = pd.DataFrame({'date_id': all_dates})
dim_date['year'] = dim_date['date_id'].dt.year
dim_date['month'] = dim_date['date_id'].dt.month
dim_date['quarter'] = dim_date['date_id'].dt.quarter
dim_date['is_weekday'] = dim_date['date_id'].dt.dayofweek < 5
dim_date['date_id'] = dim_date['date_id'].dt.strftime('%Y-%m-%d')
dim_date.to_csv(processed_dir / 'dim_date.csv', index=False)

# LOAD TO SQLITE
print("Loading into SQLite database...")
db_path = db_dir / 'bluestock_mf.db'
db_path = db_path.resolve()
if db_path.exists():
    try:
        db_path.unlink() # Start fresh
    except PermissionError:
        pass

schema_path = Path('../sql/schema.sql')
with sqlite3.connect(db_path) as conn:
    if schema_path.exists():
        with open(schema_path, 'r') as f:
            conn.executescript(f.read())
            
    df_fund.to_sql('dim_fund', conn, if_exists='append', index=False)
    dim_date.to_sql('dim_date', conn, if_exists='append', index=False)

    df_nav_db = df_nav_clean.copy()
    df_nav_db['nav_date'] = pd.to_datetime(df_nav_db['date']).dt.strftime('%Y-%m-%d')
    df_nav_db = df_nav_db[['amfi_code', 'nav_date', 'nav']]
    df_nav_db.to_sql('fact_nav', conn, if_exists='append', index=False)

    df_txn.to_sql('fact_transactions', conn, if_exists='append', index=False)
    df_perf.to_sql('fact_performance', conn, if_exists='append', index=False)

    df_port = pd.read_csv(processed_dir / '09_portfolio_holdings_clean.csv')
    df_port.to_sql('fact_portfolio', conn, if_exists='append', index=False)

    df_aum = pd.read_csv(processed_dir / '03_aum_by_fund_house_clean.csv')
    df_aum.to_sql('fact_aum', conn, if_exists='append', index=False)

print("Data Cleaning and Database Load Completed Successfully!")
