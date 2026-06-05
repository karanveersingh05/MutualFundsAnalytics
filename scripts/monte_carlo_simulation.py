import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Set visualization style
sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

# Define paths
data_dir = Path('data/processed')
charts_dir = Path('reports/charts')
charts_dir.mkdir(parents=True, exist_ok=True)

# Load clean NAV history and Fund Master
nav_df = pd.read_csv(data_dir / '02_nav_history_clean.csv')
fund_master = pd.read_csv(data_dir / '01_fund_master_clean.csv')

# Select 5 key funds
selected_funds = [
    125497, # HDFC Top 100
    119551, # SBI Bluechip
    120503, # ICICI Bluechip
    118632, # Nippon Large Cap
    119092  # Axis Bluechip
]

fund_names = fund_master.set_index('amfi_code')['scheme_name'].to_dict()

# Filter data
nav_df = nav_df[nav_df['amfi_code'].isin(selected_funds)].copy()
nav_df['date'] = pd.to_datetime(nav_df['date'])
nav_df = nav_df.sort_values(['amfi_code', 'date'])

# Calculate daily log returns
nav_df['log_return'] = nav_df.groupby('amfi_code')['nav'].apply(lambda x: np.log(x / x.shift(1))).reset_index(level=0, drop=True)
nav_df = nav_df.dropna()

# Calculate Historical Statistics (Drift and Volatility)
stats = nav_df.groupby('amfi_code')['log_return'].agg(['mean', 'std', 'var'])

# Monte Carlo Parameters
NUM_SIMULATIONS = 1000
TRADING_DAYS_PER_YEAR = 252
YEARS = 5
NUM_DAYS = TRADING_DAYS_PER_YEAR * YEARS

results = {}

for code in selected_funds:
    name = fund_names.get(code, str(code))
    
    u = stats.loc[code, 'mean']
    var = stats.loc[code, 'var']
    stdev = stats.loc[code, 'std']
    
    drift = u - (0.5 * var)
    last_nav = nav_df[nav_df['amfi_code'] == code]['nav'].iloc[-1]
    
    Z = np.random.normal(0, 1, (NUM_DAYS, NUM_SIMULATIONS))
    daily_returns = np.exp(drift + stdev * Z)
    
    price_paths = np.zeros_like(daily_returns)
    price_paths[0] = last_nav
    
    for t in range(1, NUM_DAYS):
        price_paths[t] = price_paths[t-1] * daily_returns[t]
        
    results[code] = {
        'name': name,
        'paths': price_paths,
        'last_nav': last_nav
    }

print("Monte Carlo simulation completed for 5 years.")

# Plotting the simulations and uncertainty bands
fig, axes = plt.subplots(5, 1, figsize=(14, 25))

for i, code in enumerate(selected_funds):
    name = results[code]['name']
    paths = results[code]['paths']
    last_nav = results[code]['last_nav']
    ax = axes[i]
    
    p5 = np.percentile(paths, 5, axis=1)
    p50 = np.percentile(paths, 50, axis=1)
    p95 = np.percentile(paths, 95, axis=1)
    days = np.arange(NUM_DAYS)
    
    ax.plot(days, paths[:, :100], color='gray', alpha=0.05)
    ax.plot(days, p50, color='blue', label='Median Projection (50th)')
    ax.plot(days, p95, color='green', linestyle='--', label='Optimistic (95th)')
    ax.plot(days, p5, color='red', linestyle='--', label='Pessimistic (5th)')
    
    ax.set_title(f'5-Year Monte Carlo Projection: {name} (Current NAV: ₹{last_nav:.2f})', fontsize=14, fontweight='bold')
    ax.set_xlabel('Trading Days')
    ax.set_ylabel('Projected NAV (₹)')
    ax.legend(loc='upper left')

plt.tight_layout()
plt.savefig(charts_dir / 'monte_carlo_bands.png', dpi=300)

summary = []
for code in selected_funds:
    paths = results[code]['paths']
    final_navs = paths[-1, :]
    
    summary.append({
        'Scheme': results[code]['name'],
        'Current NAV': round(results[code]['last_nav'], 2),
        '5th Percentile (Worst)': round(np.percentile(final_navs, 5), 2),
        '50th Percentile (Expected)': round(np.percentile(final_navs, 50), 2),
        '95th Percentile (Best)': round(np.percentile(final_navs, 95), 2)
    })

summary_df = pd.DataFrame(summary)
summary_df.to_csv(data_dir / 'monte_carlo_summary.csv', index=False)
print("Saved summary to data/processed/monte_carlo_summary.csv and charts/monte_carlo_bands.png")
