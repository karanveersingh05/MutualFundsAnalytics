import nbformat as nbf

nb = nbf.v4.new_notebook()

text1 = """\
# Bonus Challenge B3: Monte Carlo Simulation
**Projecting NAV growth over 5 years with uncertainty bands**

In this notebook, we perform a Monte Carlo simulation for 5 selected mutual funds.
We use historical daily returns to compute the drift and volatility, and then simulate 1,000 potential future paths over the next 5 years (1,260 trading days). We will plot the uncertainty bands (5th, 50th, and 95th percentiles).
"""

code1 = """\
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Set visualization style
sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

# Define paths
data_dir = Path('../data/processed')
charts_dir = Path('../reports/charts')
charts_dir.mkdir(parents=True, exist_ok=True)
"""

code2 = """\
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

nav_df.head()
"""

code3 = """\
# Calculate daily log returns
nav_df['log_return'] = nav_df.groupby('amfi_code')['nav'].apply(lambda x: np.log(x / x.shift(1))).reset_index(level=0, drop=True)
nav_df = nav_df.dropna()

# Calculate Historical Statistics (Drift and Volatility)
stats = nav_df.groupby('amfi_code')['log_return'].agg(['mean', 'std', 'var'])
stats
"""

code4 = """\
# Monte Carlo Parameters
NUM_SIMULATIONS = 1000
TRADING_DAYS_PER_YEAR = 252
YEARS = 5
NUM_DAYS = TRADING_DAYS_PER_YEAR * YEARS

results = {}

for code in selected_funds:
    name = fund_names.get(code, str(code))
    
    # Get historical stats
    u = stats.loc[code, 'mean']
    var = stats.loc[code, 'var']
    stdev = stats.loc[code, 'std']
    
    # Drift = mean - (0.5 * var)
    drift = u - (0.5 * var)
    
    # Get last NAV
    last_nav = nav_df[nav_df['amfi_code'] == code]['nav'].iloc[-1]
    
    # Generate random variables Z ~ N(0, 1)
    Z = np.random.normal(0, 1, (NUM_DAYS, NUM_SIMULATIONS))
    
    # Calculate daily returns
    daily_returns = np.exp(drift + stdev * Z)
    
    # Simulate price paths
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
"""

code5 = """\
# Plotting the simulations and uncertainty bands
fig, axes = plt.subplots(5, 1, figsize=(14, 25))

for i, code in enumerate(selected_funds):
    name = results[code]['name']
    paths = results[code]['paths']
    last_nav = results[code]['last_nav']
    
    ax = axes[i]
    
    # Calculate Percentiles
    p5 = np.percentile(paths, 5, axis=1)
    p50 = np.percentile(paths, 50, axis=1)
    p95 = np.percentile(paths, 95, axis=1)
    
    days = np.arange(NUM_DAYS)
    
    # Plot first 100 paths lightly
    ax.plot(days, paths[:, :100], color='gray', alpha=0.05)
    
    # Plot Median and Confidence Intervals
    ax.plot(days, p50, color='blue', label='Median Projection (50th)')
    ax.plot(days, p95, color='green', linestyle='--', label='Optimistic (95th)')
    ax.plot(days, p5, color='red', linestyle='--', label='Pessimistic (5th)')
    
    ax.set_title(f'5-Year Monte Carlo Projection: {name} (Current NAV: ₹{last_nav:.2f})', fontsize=14, fontweight='bold')
    ax.set_xlabel('Trading Days')
    ax.set_ylabel('Projected NAV (₹)')
    ax.legend(loc='upper left')

plt.tight_layout()
plt.savefig(charts_dir / 'monte_carlo_bands.png', dpi=300)
plt.show()
"""

text2 = """\
## Summary of Projections
We can summarize the final projected NAV after 5 years to compare worst-case, expected, and best-case scenarios.
"""

code6 = """\
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
summary_df
"""

nb['cells'] = [
    nbf.v4.new_markdown_cell(text1),
    nbf.v4.new_code_cell(code1),
    nbf.v4.new_code_cell(code2),
    nbf.v4.new_code_cell(code3),
    nbf.v4.new_code_cell(code4),
    nbf.v4.new_code_cell(code5),
    nbf.v4.new_markdown_cell(text2),
    nbf.v4.new_code_cell(code6)
]

with open('notebooks/monte_carlo_simulation.ipynb', 'w', encoding='utf-8') as f:
    nbf.write(nb, f)
print("Notebook generated successfully!")
