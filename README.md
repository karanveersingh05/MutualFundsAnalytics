# Bluestock Mutual Fund Analytics Platform

> **Capstone Project - Bluestock Fintech**
> End-to-end data engineering and analytics platform for Indian Mutual Funds.

---

## Overview

This project delivers a complete analytical pipeline covering:
- Automated ETL from raw AMFI/NSE data sources
- Star-schema SQLite database (`bluestock_mf.db`)
- Exploratory Data Analysis with 12+ visualisations
- Fund performance metrics: CAGR, Sharpe, Sortino, Alpha, Beta, Max Drawdown
- Fund Scorecard (0-100 composite ranking)
- Advanced Risk Analytics: VaR/CVaR, Rolling Sharpe, Cohort Analysis, SIP Continuity, HHI
- CLI-based Fund Recommender by risk appetite
- Power BI-ready dashboard mockups and PDF report

---

## Project Structure

```
MutualFundsAnalytics/
├── data/
│   ├── raw/            # 10 source CSVs + live NAV files
│   ├── processed/      # Cleaned CSVs + computed outputs
│   └── db/             # bluestock_mf.db (SQLite)
├── notebooks/
│   ├── 03_eda_analysis.ipynb
│   ├── 04_performance_analytics.ipynb
│   └── 05_advanced_analytics.ipynb
├── reports/
│   ├── charts/         # 12 PNG chart exports
│   ├── Final_Report.pdf
│   └── Bluestock_MF_Presentation.pptx
├── scripts/
│   ├── live_nav_fetch.py         # Live NAV API ingestor
│   ├── data_ingestion.py         # Raw data loader + validator
│   ├── data_cleaning.py          # ETL cleaner + SQLite loader
│   ├── run_eda.py                # 12-chart EDA generator
│   ├── compute_metrics.py        # Fund performance metrics + scorecard
│   ├── generate_advanced_analytics.py  # VaR, Rolling Sharpe, HHI, Cohort
│   ├── recommender.py            # CLI fund recommender
│   ├── generate_dashboard_mocks.py     # Dashboard page PNGs + PDF
│   └── generate_final_docs.py    # Final report + presentation files
├── sql/
│   ├── schema.sql      # Star schema DDL
│   └── queries.sql     # 10 analytical SQL queries
├── dashboard/          # Power BI mockup files + PDF
├── run_pipeline.py     # Master execution script
├── requirements.txt
└── data_dictionary.md
```

---

## Setup

```bash
# 1. Clone the repository
git clone https://github.com/karanveersingh05/MutualFundsAnalytics.git
cd MutualFundsAnalytics

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the full pipeline
python run_pipeline.py
```

---

## Running Individual Scripts

```bash
# ETL only
cd scripts && python data_cleaning.py

# EDA charts
cd scripts && python run_eda.py

# Performance metrics & scorecard
cd scripts && python compute_metrics.py

# Advanced analytics (VaR, Cohort, HHI)
cd scripts && python generate_advanced_analytics.py

# Fund Recommender
python scripts/recommender.py --risk High     # Options: Low | Moderate | High
```

---

## Database Schema (Star Schema)

| Table | Type | Key Metric |
|---|---|---|
| `dim_fund` | Dimension | 40 schemes, fund metadata |
| `dim_date` | Dimension | 1,608 calendar days |
| `fact_nav` | Fact | 64,320 daily NAV records |
| `fact_transactions` | Fact | 32,778 investor transactions |
| `fact_performance` | Fact | 40 scheme performance metrics |
| `fact_portfolio` | Fact | 322 portfolio holdings |
| `fact_aum` | Fact | 90 AUM data points by fund house |

---

## Dataset Descriptions

| File | Description |
|---|---|
| `01_fund_master.csv` | Reference table: fund house, category, expense ratio, risk grade |
| `02_nav_history.csv` | Daily NAV for 40 schemes (2022-2026) |
| `03_aum_by_fund_house.csv` | Quarterly AUM by AMC (2022-2025) |
| `04_monthly_sip_inflows.csv` | Industry SIP inflow data (Jan 2022 - Dec 2025) |
| `05_category_inflows.csv` | Net fund category inflows by month |
| `06_industry_folio_count.csv` | Total folios, equity/debt/hybrid split |
| `07_scheme_performance.csv` | Return metrics, Sharpe, Sortino, Alpha, Beta |
| `08_investor_transactions.csv` | 32K+ investor SIP/Lumpsum/Redemption records |
| `09_portfolio_holdings.csv` | Stock-level portfolio weights per fund |
| `10_benchmark_indices.csv` | Nifty 50, Nifty 100, Midcap, Smallcap index data |

---

## Key Results

- **SIP ATH**: Rs 31,002 Cr in December 2025
- **Folio Growth**: 13.26 Cr (Jan 2022) → 26.12 Cr (Dec 2025)
- **AUM Leader**: SBI Mutual Fund at Rs 12.5 Lakh Crore
- **Top Scorecard Fund**: ICICI Pru Midcap - Score: 100/100
- **Best Sharpe**: Mirae Asset Large Cap (Sharpe: 1.07)
- **Highest HHI (Concentration)**: Axis Bluechip Fund (HHI: 2065)

---

## Dashboard

The `dashboard/` directory contains:
- `bluestock_mf_dashboard.pbix` - Power BI source file
- `Dashboard.pdf` - 4-page dashboard PDF export
- `Page_1_Industry_Overview.png` through `Page_4_SIP_Market_Trends.png`

---

*Built by Karan Veer Singh | Bluestock Fintech Capstone | June 2026*
