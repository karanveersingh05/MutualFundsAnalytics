import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Paths
data_dir = Path('data/processed')
charts_dir = Path('reports/charts')
charts_dir.mkdir(parents=True, exist_ok=True)

nav_df = pd.read_csv(data_dir / '02_nav_history_clean.csv')
fund_master = pd.read_csv(data_dir / '01_fund_master_clean.csv')

# Select 5 diverse funds for the portfolio
selected_funds = [
    119551, # SBI Bluechip (Large Cap)
    100033, # HDFC Mid-Cap (Mid Cap)
    118634, # Nippon Small Cap (Small Cap)
    120507, # ICICI Liquid (Liquid)
    119120  # SBI Magnum Gilt (Gilt)
]

fund_names = fund_master.set_index('amfi_code')['scheme_name'].to_dict()

# Pivot data to get a daily NAV matrix (rows = dates, columns = funds)
nav_pivot = nav_df[nav_df['amfi_code'].isin(selected_funds)].pivot(index='date', columns='amfi_code', values='nav')
nav_pivot = nav_pivot.dropna() # Keep only overlapping dates

# Calculate daily log returns
returns = np.log(nav_pivot / nav_pivot.shift(1)).dropna()

# Annualize metrics
mean_returns = returns.mean() * 252
cov_matrix = returns.cov() * 252

# Simulation params
NUM_PORTFOLIOS = 10000
RISK_FREE_RATE = 0.06

# Arrays to store results
results = np.zeros((3, NUM_PORTFOLIOS))
weights_record = []

for i in range(NUM_PORTFOLIOS):
    weights = np.random.random(len(selected_funds))
    weights /= np.sum(weights)
    
    port_return = np.sum(mean_returns * weights)
    port_volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
    sharpe_ratio = (port_return - RISK_FREE_RATE) / port_volatility
    
    results[0,i] = port_return
    results[1,i] = port_volatility
    results[2,i] = sharpe_ratio
    weights_record.append(weights)

# Find optimal portfolios
max_sharpe_idx = np.argmax(results[2])
min_vol_idx = np.argmin(results[1])

opt_sharpe_w = weights_record[max_sharpe_idx]
opt_vol_w = weights_record[min_vol_idx]

# Save weights to CSV
allocations = []
for idx, code in enumerate(nav_pivot.columns):
    allocations.append({
        'amfi_code': code,
        'scheme_name': fund_names.get(code, str(code)),
        'max_sharpe_weight_pct': round(opt_sharpe_w[idx] * 100, 2),
        'min_volatility_weight_pct': round(opt_vol_w[idx] * 100, 2)
    })
pd.DataFrame(allocations).to_csv(data_dir / 'optimal_portfolio.csv', index=False)

# Plotting
sns.set_theme(style="whitegrid")
plt.figure(figsize=(12, 7))
sc = plt.scatter(results[1,:], results[0,:], c=results[2,:], cmap='viridis', marker='o', s=10, alpha=0.5)
plt.colorbar(sc, label='Sharpe Ratio')
plt.scatter(results[1, max_sharpe_idx], results[0, max_sharpe_idx], color='r', marker='*', s=400, label='Max Sharpe Ratio', edgecolor='black')
plt.scatter(results[1, min_vol_idx], results[0, min_vol_idx], color='b', marker='*', s=400, label='Min Volatility', edgecolor='black')

plt.title('Markowitz Efficient Frontier (10,000 Portfolios)', fontsize=14, fontweight='bold')
plt.xlabel('Expected Volatility (Risk)')
plt.ylabel('Expected Return (CAGR)')
plt.legend(labelspacing=1.2)
plt.tight_layout()
plt.savefig(charts_dir / 'efficient_frontier.png', dpi=300)
print("Markowitz Optimization completed successfully.")
