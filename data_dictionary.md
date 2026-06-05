# Data Dictionary - Bluestock Mutual Fund Analytics

## Table: dim_fund
- `amfi_code` (INTEGER, PK): Unique AMFI scheme identifier.
- `fund_house` (TEXT): Name of the AMC (e.g., SBI, HDFC).
- `scheme_name` (TEXT): Official name of the mutual fund scheme.
- `category` (TEXT): Broad category (Equity, Debt, Hybrid).
- `sub_category` (TEXT): Specific category classification.
- `plan` (TEXT): Direct or Regular plan.
- `launch_date` (DATE): Inception date of the fund.
- `benchmark` (TEXT): Fund's benchmark index.
- `expense_ratio_pct` (REAL): Annual expense ratio (%).
- `exit_load_pct` (REAL): Exit load penalty (%).
- `fund_manager` (TEXT): Primary manager name.
- `risk_category` (TEXT): Risk-o-meter classification.
- `sebi_category_code` (TEXT): Internal SEBI classification code.

## Table: dim_date
- `date_id` (DATE, PK): The standard YYYY-MM-DD date.
- `year` (INTEGER): Calendar year.
- `month` (INTEGER): Calendar month (1-12).
- `quarter` (INTEGER): Calendar quarter (1-4).
- `is_weekday` (BOOLEAN): True if Mon-Fri, False if Sat-Sun.

## Table: fact_nav
- `nav_id` (INTEGER, PK): Auto-incremented primary key.
- `amfi_code` (INTEGER, FK): Reference to dim_fund.
- `nav_date` (DATE, FK): Date of the Net Asset Value.
- `nav` (REAL): Daily Net Asset Value (in INR).

## Table: fact_transactions
- `transaction_id` (INTEGER, PK): Auto-incremented primary key.
- `investor_id` (TEXT): Unique investor ID.
- `transaction_date` (DATE, FK): Date of transaction.
- `amfi_code` (INTEGER, FK): Reference to dim_fund.
- `transaction_type` (TEXT): Type of transaction (SIP/Lumpsum/Redemption).
- `amount_inr` (REAL): Transaction amount in INR.
- `state`, `city`, `city_tier`, `age_group`, `gender`, `annual_income_lakh`, `payment_mode`, `kyc_status` (TEXT/REAL): Demographic and KYC fields.

## Table: fact_performance
- `amfi_code` (INTEGER, PK, FK): Reference to dim_fund.
- `return_1yr_pct`, `return_3yr_pct`, `return_5yr_pct` (REAL): Historical CAGR returns.
- `benchmark_3yr_pct` (REAL): Benchmark 3-year return.
- `alpha`, `beta`, `sharpe_ratio`, `sortino_ratio`, `std_dev_ann_pct`, `max_drawdown_pct` (REAL): Computed risk metrics.
- `morningstar_rating` (INTEGER): Rating out of 5 stars.

## Table: fact_portfolio
- `portfolio_id` (INTEGER, PK): Auto-incremented primary key.
- `amfi_code` (INTEGER, FK): Reference to dim_fund.
- `stock_symbol`, `stock_name`, `sector` (TEXT): Equity asset details.
- `weight_pct` (REAL): Allocation percentage in portfolio.
- `market_value_cr` (REAL): Holdings market value (Crores).
- `current_price_inr` (REAL): Current traded price of the stock.
- `portfolio_date` (DATE): Date of portfolio disclosure.
