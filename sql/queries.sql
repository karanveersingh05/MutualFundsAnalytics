-- 1. Count of funds by category
SELECT category, count(*) as num_funds FROM dim_fund GROUP BY category;

-- 2. Average expense ratio by fund house
SELECT fund_house, AVG(expense_ratio_pct) as avg_expense FROM dim_fund GROUP BY fund_house ORDER BY avg_expense ASC;

-- 3. Top 5 funds with best 3-year return
SELECT f.scheme_name, p.return_3yr_pct FROM fact_performance p JOIN dim_fund f ON p.amfi_code = f.amfi_code ORDER BY p.return_3yr_pct DESC LIMIT 5;

-- 4. Total SIP transactions by state
SELECT state, SUM(amount_inr) as total_sip_amount FROM fact_transactions WHERE transaction_type = 'SIP' GROUP BY state ORDER BY total_sip_amount DESC;

-- 5. Funds with expense_ratio < 1%
SELECT scheme_name, expense_ratio_pct FROM dim_fund WHERE expense_ratio_pct < 1.0;

-- 6. Max NAV for HDFC Top 100 (Code: 125497)
SELECT MAX(nav) as max_nav FROM fact_nav WHERE amfi_code = 125497;

-- 7. Total Redemption Amount by Age Group
SELECT age_group, SUM(amount_inr) as redemption_amount FROM fact_transactions WHERE transaction_type = 'Redemption' GROUP BY age_group ORDER BY redemption_amount DESC;

-- 8. Count of SIP vs Lumpsum transactions
SELECT transaction_type, COUNT(*) as txn_count FROM fact_transactions GROUP BY transaction_type;

-- 9. Top 5 sectors invested by mutual funds
SELECT sector, SUM(market_value_cr) as total_market_value FROM fact_portfolio GROUP BY sector ORDER BY total_market_value DESC LIMIT 5;

-- 10. Average Sharpe ratio by Risk Category
SELECT f.risk_category, AVG(p.sharpe_ratio) as avg_sharpe FROM fact_performance p JOIN dim_fund f ON p.amfi_code = f.amfi_code GROUP BY f.risk_category;
