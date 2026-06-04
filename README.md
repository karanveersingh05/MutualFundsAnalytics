# Bluestock Mutual Fund Analytics Platform

## Overview
An end-to-end data analytics platform for Indian Mutual Funds. This project encompasses automated data ingestion, cleaning, a star-schema SQLite database, advanced financial performance metrics, and a Power BI dashboard.

## Setup Instructions
1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`
3. Run the master pipeline script: `python run_pipeline.py`

## Project Structure
- `data/`: Raw and processed CSVs, SQLite DB.
- `notebooks/`: Jupyter Notebooks for EDA and Advanced Analytics.
- `reports/`: Final reports, presentations, and exported charts.
- `scripts/`: Python scripts for ETL and metrics computation.
- `sql/`: Schema and query definitions.
- `dashboard/`: Power BI dashboard mockups and source file.

## Dataset Descriptions
- `01_fund_master`: Reference details for all schemes.
- `02_nav_history`: Daily NAV values.
- `03_aum_by_fund_house`: Quarterly AUM figures.
- `04_monthly_sip_inflows`: Macro industry SIP inflows.
- `07_scheme_performance`: Fund-level return metrics.
- `08_investor_transactions`: Detailed transaction logs.

## Dashboard
The `bluestock_mf_dashboard.pbix` is located in the `dashboard/` directory. (Mock files generated for automated environment delivery).
