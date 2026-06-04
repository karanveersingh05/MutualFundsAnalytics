"""
data_cleaning.py
Cleans all raw CSVs and loads them into the SQLite star-schema database.
"""
import pandas as pd
import numpy as np
import sqlite3
from pathlib import Path

# Paths relative to this script's location
BASE_DIR = Path(__file__).parent.parent
raw_dir      = BASE_DIR / 'data' / 'raw'
processed_dir = BASE_DIR / 'data' / 'processed'
db_dir        = BASE_DIR / 'data' / 'db'
schema_path   = BASE_DIR / 'sql' / 'schema.sql'

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

def fill_missing_dates(group, amfi_code_val):
    """Forward-fill NAV for weekends and holidays within each fund."""
    group = group.set_index('date')
    group = group.reindex(all_dates)
    group['nav'] = group['nav'].ffill()
    group = group.reset_index().rename(columns={'index': 'date'})
    group['amfi_code'] = amfi_code_val
    return group

# Apply per-fund ffill, passing the amfi_code via lambda
df_nav_clean = pd.concat([
    fill_missing_dates(grp[['date', 'nav']], code)
    for code, grp in df_nav.groupby('amfi_code')
], ignore_index=True)
df_nav_clean.to_csv(processed_dir / '02_nav_history_clean.csv', index=False)
print(f"  NAV rows: {len(df_nav_clean):,}")

# 2. Clean investor_transactions.csv
print("Cleaning investor_transactions.csv...")
df_txn = pd.read_csv(raw_dir / '08_investor_transactions.csv')
df_txn['transaction_type'] = df_txn['transaction_type'].str.strip().str.title()
# Ensure SIP stays uppercase
df_txn['transaction_type'] = df_txn['transaction_type'].replace({'Sip': 'SIP'})
df_txn = df_txn[df_txn['amount_inr'] > 0]
df_txn['transaction_date'] = pd.to_datetime(df_txn['transaction_date']).dt.strftime('%Y-%m-%d')
df_txn['kyc_status'] = df_txn['kyc_status'].str.strip().str.title()
df_txn.to_csv(processed_dir / '08_investor_transactions_clean.csv', index=False)
print(f"  Transaction rows: {len(df_txn):,}")

# 3. Clean scheme_performance.csv
print("Cleaning scheme_performance.csv...")
df_perf = pd.read_csv(raw_dir / '07_scheme_performance.csv')
numeric_cols = [
    'return_1yr_pct', 'return_3yr_pct', 'return_5yr_pct',
    'alpha', 'beta', 'sharpe_ratio', 'sortino_ratio',
    'std_dev_ann_pct', 'max_drawdown_pct', 'expense_ratio_pct'
]
for col in numeric_cols:
    df_perf[col] = pd.to_numeric(df_perf[col], errors='coerce')
# Validate expense_ratio range
bad_expense = (df_perf['expense_ratio_pct'] < 0.1) | (df_perf['expense_ratio_pct'] > 2.5)
if bad_expense.any():
    print(f"  WARNING: {bad_expense.sum()} schemes have expense_ratio outside 0.1-2.5% — clipping.")
    df_perf['expense_ratio_pct'] = df_perf['expense_ratio_pct'].clip(lower=0.1, upper=2.5)
df_perf.to_csv(processed_dir / '07_scheme_performance_clean.csv', index=False)
print(f"  Performance rows: {len(df_perf):,}")

# 4. Clean fund_master.csv
print("Cleaning 01_fund_master.csv...")
df_fund = pd.read_csv(raw_dir / '01_fund_master.csv')
df_fund['expense_ratio_pct'] = pd.to_numeric(df_fund['expense_ratio_pct'], errors='coerce')
df_fund['expense_ratio_pct'] = df_fund['expense_ratio_pct'].clip(lower=0.1, upper=2.5)
df_fund.to_csv(processed_dir / '01_fund_master_clean.csv', index=False)
print(f"  Fund master rows: {len(df_fund):,}")

# 5. Pass-through for remaining datasets
print("Copying remaining datasets to processed...")
rest_files = [
    '03_aum_by_fund_house.csv',
    '04_monthly_sip_inflows.csv',
    '05_category_inflows.csv',
    '06_industry_folio_count.csv',
    '09_portfolio_holdings.csv',
    '10_benchmark_indices.csv',
]
for f in rest_files:
    df = pd.read_csv(raw_dir / f)
    out = processed_dir / f.replace('.csv', '_clean.csv')
    df.to_csv(out, index=False)
    print(f"  {f}: {len(df):,} rows")

# 6. dim_date generation
print("Generating dim_date...")
dim_date = pd.DataFrame({'date_id': all_dates})
dim_date['year']       = dim_date['date_id'].dt.year
dim_date['month']      = dim_date['date_id'].dt.month
dim_date['quarter']    = dim_date['date_id'].dt.quarter
dim_date['is_weekday'] = dim_date['date_id'].dt.dayofweek < 5
dim_date['date_id']    = dim_date['date_id'].dt.strftime('%Y-%m-%d')
dim_date.to_csv(processed_dir / 'dim_date.csv', index=False)
print(f"  dim_date rows: {len(dim_date):,}")

# 7. Load into SQLite
print("Loading into SQLite database...")
db_path = (db_dir / 'bluestock_mf.db').resolve()
if db_path.exists():
    try:
        db_path.unlink()
    except PermissionError:
        print("  WARNING: Could not delete existing DB (file locked). Data will be appended.")

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

    # Verify row counts
    for table in ['dim_fund', 'dim_date', 'fact_nav', 'fact_transactions', 'fact_performance']:
        count = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        print(f"  DB [{table}]: {count:,} rows")

print("Data Cleaning and Database Load Completed Successfully!")
