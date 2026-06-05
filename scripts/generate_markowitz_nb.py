import nbformat as nbf

nb = nbf.v4.new_notebook()

text1 = """\
# Bonus Challenge B4: Markowitz Efficient Frontier
**Portfolio Optimization Module**

In this notebook, we calculate the optimal asset allocation for a diverse basket of mutual funds using Modern Portfolio Theory (MPT).
We will simulate 10,000 random portfolios to construct the Efficient Frontier and identify:
1. The portfolio with the **Maximum Sharpe Ratio** (Best risk-adjusted return).
2. The portfolio with the **Minimum Volatility** (Lowest risk).
"""

code1 = """\
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (12, 7)

data_dir = Path('../data/processed')
charts_dir = Path('../reports/charts')
charts_dir.mkdir(parents=True, exist_ok=True)
"""

code2 = """\
# Load data
nav_df = pd.read_csv(data_dir / '02_nav_history_clean.csv')
fund_master = pd.read_csv(data_dir / '01_fund_master_clean.csv')

# Select a highly diverse basket of 5 funds
selected_funds = [
    119551, # SBI Bluechip (Large Cap)
    100033, # HDFC Mid-Cap (Mid Cap)
    118634, # Nippon Small Cap (Small Cap)
    120507, # ICICI Liquid (Liquid/Debt)
    119120  # SBI Magnum Gilt (Long Term Gilt)
]

fund_names = fund_master.set_index('amfi_code')['scheme_name'].to_dict()

# Pivot data to wide format (dates x funds)
nav_pivot = nav_df[nav_df['amfi_code'].isin(selected_funds)].pivot(index='date', columns='amfi_code', values='nav')
nav_pivot = nav_pivot.dropna() # Keep dates where all funds existed

# Calculate log returns
returns = np.log(nav_pivot / nav_pivot.shift(1)).dropna()

# Annualize Mean Returns and Covariance Matrix
mean_returns = returns.mean() * 252
cov_matrix = returns.cov() * 252

print("Annualized Expected Returns:\\n", mean_returns)
"""

code3 = """\
# Monte Carlo Simulation for Portfolios
NUM_PORTFOLIOS = 10000
RISK_FREE_RATE = 0.06

results = np.zeros((3, NUM_PORTFOLIOS))
weights_record = []

np.random.seed(42)

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

# Identify Optimal Portfolios
max_sharpe_idx = np.argmax(results[2])
min_vol_idx = np.argmin(results[1])

opt_sharpe_w = weights_record[max_sharpe_idx]
opt_vol_w = weights_record[min_vol_idx]

print("Simulated 10,000 Portfolios.")
"""

text2 = """\
## Visualizing the Efficient Frontier
We plot all 10,000 portfolios on a scatter plot. The portfolios forming the upper left boundary represent the "Efficient Frontier."
"""

code4 = """\
plt.figure(figsize=(12, 7))
sc = plt.scatter(results[1,:], results[0,:], c=results[2,:], cmap='viridis', marker='o', s=10, alpha=0.5)
plt.colorbar(sc, label='Sharpe Ratio')
plt.scatter(results[1, max_sharpe_idx], results[0, max_sharpe_idx], color='r', marker='*', s=400, label='Max Sharpe Ratio', edgecolor='black')
plt.scatter(results[1, min_vol_idx], results[0, min_vol_idx], color='b', marker='*', s=400, label='Min Volatility', edgecolor='black')

plt.title('Markowitz Efficient Frontier', fontsize=16, fontweight='bold')
plt.xlabel('Expected Volatility (Annualized Risk)')
plt.ylabel('Expected Return (Annualized CAGR)')
plt.legend(labelspacing=1.2)
plt.tight_layout()
plt.savefig(charts_dir / 'efficient_frontier.png', dpi=300)
plt.show()
"""

text3 = """\
## Optimal Asset Allocations
Let's review the exact weight percentages required to achieve the Maximum Sharpe Ratio and Minimum Volatility portfolios.
"""

code5 = """\
allocations = []
for idx, code in enumerate(nav_pivot.columns):
    allocations.append({
        'Scheme Name': fund_names.get(code, str(code)),
        'Max Sharpe Weight (%)': round(opt_sharpe_w[idx] * 100, 2),
        'Min Volatility Weight (%)': round(opt_vol_w[idx] * 100, 2)
    })
    
alloc_df = pd.DataFrame(allocations)
alloc_df.to_csv(data_dir / 'optimal_portfolio.csv', index=False)
alloc_df
"""

nb['cells'] = [
    nbf.v4.new_markdown_cell(text1),
    nbf.v4.new_code_cell(code1),
    nbf.v4.new_code_cell(code2),
    nbf.v4.new_code_cell(code3),
    nbf.v4.new_markdown_cell(text2),
    nbf.v4.new_code_cell(code4),
    nbf.v4.new_markdown_cell(text3),
    nbf.v4.new_code_cell(code5)
]

with open('notebooks/markowitz_optimization.ipynb', 'w', encoding='utf-8') as f:
    nbf.write(nb, f)
print("Notebook generated successfully!")
