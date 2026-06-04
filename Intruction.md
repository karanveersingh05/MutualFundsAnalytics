overview:
Mutual Fund Analytics
ACTIVE
Total Tasks
8	
Exploratory Data Analysis (EDA)	
11 June
Project Setup + Data Ingestion (ETL)		
03 June
Data Cleaning + SQL Database Design		
06 June
Advanced Analytics + Risk Metrics		
18 June
Fund Performance Analytics		
13 June
Dashboard Development (Power BI / Tableau)		
16 June
DELIVERABLES & EVALUATION RUBRIC	
22 June
Final Report + Presentation + Deployment		
21 June
 

 description:
 📊 Mutual Fund Analytics Platform
Capstone Project — Bluestock Fintech Pvt. Ltd.
🏆 Individual Capstone | 7 Days (~50–55 hrs)
🔓 Full data pipeline · AMFI + mfapi.in · Real Indian MF data
📌 Project DNA
Build a full-stack Mutual Fund Analytics Platform using publicly available Indian mutual fund data from AMFI India and mfapi.in. Design and implement a complete data pipeline: ingest raw NAV, AUM, and SIP data → clean & load into relational DB → exploratory & performance analytics → interactive Power BI / Tableau dashboard.

🏛️ 10 Real AMCs
SBI MF, HDFC MF, ICICI Prudential, Nippon India, Kotak, Axis, Aditya Birla Sun Life, UTI, Mirae Asset, DSP MF — anchored to AMFI figures (SBI AUM ₹12.5L Cr, industry SIP ₹31,002 Cr Dec 2025).
📈 Data Scale
40 real AMFI scheme codes · 46,000+ daily NAV records · 32,000+ investor transactions · Benchmark indices (Nifty 50, Nifty 100, BSE SmallCap) & portfolio holdings.
🔧 Tech Stack
Python 3.10+ · Pandas · NumPy · Matplotlib · Seaborn · Plotly · SQLite · SQLAlchemy · SciPy · Jupyter Lab · Power BI Desktop · Git + GitHub · mfapi.in REST API
🎯 Domain
Mutual Fund / Fintech — end-to-end analytics engineering + dashboarding (no API keys required, all public sources).
🎯 Core Objectives & Deliverables
#	Objective	Output Artifact
O1	Build Python ETL pipeline from raw AMFI / mfapi.in data	Automated .py script
O2	Design a normalised SQL star schema (5+ tables)	schema.sql
O3	Perform comprehensive EDA on NAV, AUM, SIP data	EDA notebook, 15+ charts
O4	Compute Sharpe, Sortino, Alpha, Beta, VaR, Max Drawdown	Metrics notebook + CSVs
O5	Build a 4-page interactive Power BI / Tableau dashboard	.pbix / .twbx file
O6	Analyse investor demographics and transaction patterns	Demographic insights
O7	Benchmark fund returns vs Nifty 50 / Nifty 100	Benchmark comparison chart
O8	Document and present findings	PDF report + 12-slide deck
🗃️ Provided Datasets (10 real-world files)
File	Rows	Description
01_fund_master.csv	40	40 real AMFI schemes with codes, fund house, expense ratio, benchmark, fund manager, risk grade
02_nav_history.csv	46,000	Daily NAV Jan 2022–May 2026, anchored to real mfapi.in values (e.g. HDFC Top 100 Direct code 125497)
03_aum_by_fund_house.csv	90	Quarterly AUM (₹ crore) for top 10 AMCs 2022–2025 (SBI ₹11.14L Cr Dec 2024)
04_monthly_sip_inflows.csv	48	Real AMFI Monthly Note — SIP inflows, active accounts Jan 2022–Dec 2025 incl ₹31,002 Cr milestone
05_category_inflows.csv	144	Net inflows by category (Large Cap, Mid Cap, Small Cap, ELSS, Liquid, Gilt etc.) for FY 2024–25
06_industry_folio_count.csv	21	Total MF folios (crore) — growth from 13.26 Cr (Jan 2022) to 26.12 Cr (Dec 2025)
07_scheme_performance.csv	40	1yr/3yr/5yr CAGR, Sharpe, Sortino, Alpha, Beta, Max Drawdown, Std Dev for all 40 schemes
08_investor_transactions.csv	32,000+	SIP / Lumpsum / Redemption for 5,000 investors across 12 Indian states with age, income, city tier
09_portfolio_holdings.csv	320	Top stock holdings per equity fund — stock, sector, weight %, market value
10_benchmark_indices.csv	8,050	Daily close for Nifty 50, Nifty 100, Nifty Midcap 150, BSE SmallCap, CRISIL Liquid & Gilt
📀 46k+ NAV records
💰 AUM data: ₹12.5L Cr SBI anchor
📊 SIP inflow peak: ₹31,002 Cr (Dec '25)
👥 5k investors, 12 states
⚙️ Data Pipeline & Architecture (Star Schema)
🐍 ETL Pipeline (Python)
Extract: mfapi.in REST API + local CSVs (AMFI official)
Transform: pandas cleaning, type casting, handling missing NAVs
Load: SQLite / PostgreSQL with SQLAlchemy ORM
Automated scheduling script: `etl_pipeline.py`
🗄️ Normalised Star Schema (5+ tables)
dim_fund (scheme_code, name, AMC, category, risk_grade)
fact_nav (nav_id, scheme_code, nav_date, nav_value)
fact_aum (aum_id, amc_name, quarter_date, aum_crores)
fact_sip (sip_id, month_year, sip_inflow_cr, active_accounts)
fact_transactions (txn_id, investor_id, scheme_code, amount, type)
bridge_benchmark, dim_investor, etc. → fully joinable for BI

                # 🧠 Sample transformation snippet (EDA ready)
                import pandas as pd
                nav_df = pd.read_csv('02_nav_history.csv')
                perf_df = pd.read_csv('07_scheme_performance.csv')
                merged = nav_df.merge(perf_df, on='scheme_code')
                # compute rolling volatility, Sharpe etc.
                print(merged.groupby('fund_house')['nav_return'].mean())
            
📐 Advanced Analytics — Risk & Performance Metrics
📉 Risk Metrics: Sharpe Ratio, Sortino Ratio, Value at Risk (VaR 95%), Maximum Drawdown, Beta vs Nifty 50, Alpha (Jensen).
📈 Performance KPIs: Rolling CAGR (1/3/5Y), Information Ratio, Standard Deviation, Upside Capture.
🧪 Statistical Tests: Normality of returns, correlation matrix of sectoral indices, AUM growth regression.
📊 EDA Deliverables: 15+ charts: NAV trend heatmaps, SIP account growth, category inflow treemaps, folio count explosion, AUM bar race, scatter of risk-return.
📎 Output files from metrics notebook: fund_sharpe_ranks.csv var_drawdown_summary.csv alpha_beta_table.csv
📊 BI Dashboard (Power BI / Tableau) — 4 Interactive Pages
📈 Page 1: Market Overview
— Industry AUM, Folio growth, SIP inflows timeline (₹31,002 Cr milestone), category-wise net flows. KPI cards + forecast trend.
📉 Page 2: Fund Performance & Risk
— Sharpe vs Sortino scatter, Max Drawdown bar chart, fund ranking by Alpha, rolling beta comparison against Nifty 50.
🧑‍💻 Page 3: Investor Demographics & Transactions
— Age/income distribution, city tier (Tier1/2/3), SIP vs Lumpsum pie, redemption patterns across 12 states. Choropleth map of India.
🏢 Page 4: Portfolio Holdings & Sector Exposure
— Sunburst of top holdings, sector concentration, weight % by market cap, stock-level exposure across top 5 funds.
🖥️ Demo-ready insights: “Mid-cap funds outperformed large-cap by 3.2% alpha (3Y)”, “Highest SIP contribution from Maharashtra & Karnataka”, “Equity oriented AUM growth +41% during 2023-2025”.
🏆 Benchmark & Index Comparison
Compare fund returns against Nifty 50, Nifty 100, Nifty Midcap 150, BSE SmallCap using daily benchmark indices (10_benchmark_indices.csv). Compute tracking error, relative performance line charts, and rolling 6-month correlation. Visual output: Benchmark comparison chart (O7) with interactive tooltips for each scheme.


                # Example benchmark alignment
                import plotly.express as px
                # merged_bench = fund_returns.merge(benchmark_df, on='date')
                # fig = px.line(merged_bench, title="HDFC Top 100 vs Nifty 50 Rolling Returns")
            
👥 Investor Demographics & Transaction Patterns (O6)
🔍 Key Dimensions:
Age bands: 25-34 (highest SIP penetration), 45-60 (high lumpsum)
Income buckets: ₹5-12L, ₹12-25L, ₹25L+ -> correlation with risk appetite
City tier: Tier 1 accounts 56% of total transactions, but Tier 2 growing 2.5x faster
Redemption behaviour: sharp spikes in March & November (tax harvesting?)
📌 Transaction Mix: from 08_investor_transactions.csv : SIP monthly frequency dominates (68%), systematic withdrawal plans (SWP) emerging in high-net-worth segment. Churn rate by fund house & category.
📌 States: MH, KA, TN, DL, GJ, UP, WB, etc.
🧑‍🎓 31% investors under 30 years
🏙️ Tier-2 cities: +19% YoY growth
📅 Milestone & Execution Roadmap (7 working days)
Day	Focus
Day 1-2	ETL development: connect to mfapi.in, parse CSVs, load into SQLite (40+ schemes, 46k NAV rows). Validate data quality.
Day 3	Star schema design + indexing. Write schema.sql and full database setup script. Perform initial EDA with pandas/profiling.
Day 4	Risk & performance analytics notebook: Sharpe, Sortino, VaR, MaxDD, alpha/beta, generate metric tables.
Day 5	Build interactive Power BI/Tableau dashboard (4 pages + slicers). Connect live to aggregated views.
Day 6	Demographic deep dive, benchmark comparison, fine-tuning visuals, and prepare slide deck outline.
Day 7	Documentation, final PDF report, 12-slide presentation, dashboard publishing, and GitHub repo commit.
✅ All data sources are free & publicly accessible — AMFI India, mfapi.in, NSE/BSE public indices. No API keys required, perfect for capstone showcase.

🔗 References & Resources
📡 mfapi.in REST API docs
📄 AMFI monthly SIP report (Dec 2025)
🐙 GitHub repo structure: /etl, /notebooks, /dashboard, /docs
📊 Power BI theme: fintech blue+emerald
⚡ Capstone final submission: include full Python pipeline, interactive dashboard, and a recorded walkthrough highlighting SIP surge (₹31,002 Cr milestone) and performance of top 5 equity funds vs Nifty 100.
🧠 Bluestock Fintech Capstone — Mutual Fund Analytics Platform · Data sourced from AMFI India, mfapi.in, and NSE/BSE public records · For internal evaluation & portfolio showcase.

task1:
Project Setup + Data Ingestion (ETL)
DONE
TASK
LOW
Assigned to
MY
mythiliseenivasan11
SH
shivamshrivastavadeepspace
TE
tejaswibhardwaj13
AB
abhishek.kumar529127
KS
Karan Veer Singh
Due : 03 Jun 2026
Time estimate: 6–8 hours

Tasks:

Create project folder structure: data/raw, data/processed, notebooks/, sql/, dashboard/, reports/. Initialise Git repo and push to GitHub.
Install all dependencies: pandas, numpy, matplotlib, seaborn, plotly, sqlalchemy, requests, scipy, jupyter. Create requirements.txt.
Load all 10 provided CSV datasets using Pandas. Print .shape, .dtypes, and .head() for each. Note any anomalies.
Fetch live NAV from mfapi.in: GET https://api.mfapi.in/mf/125497 (HDFC Top 100 Direct). Parse JSON response and save as raw CSV.
Fetch NAV for 5 key schemes: SBI Bluechip (119551), ICICI Bluechip (120503), Nippon Large Cap (118632), Axis Bluechip (119092), Kotak Bluechip (120841).
Explore fund master — print unique fund houses, categories, sub-categories, risk grades. Understand AMFI scheme code structure.
Validate AMFI codes — confirm every code in fund_master exists in nav_history. Write a short data quality summary.
Git commit: "Day 1: Data ingestion complete"
Deliverables: data_ingestion.py, live_nav_fetch.py, requirements.txt, GitHub repo with Day 1 commit
githublink for repo: https://github.com/karanveersingh05/MutualFundsAnalytics.git

task2:
Data Cleaning + SQL Database Design
TODO
TASK
MEDIUM
Assigned to
MY
mythiliseenivasan11
SH
shivamshrivastavadeepspace
TE
tejaswibhardwaj13
AB
abhishek.kumar529127
KS
Karan Veer Singh
Due : 06 Jun 2026
Time estimate: 7–8 hours

Tasks:

Clean nav_history.csv — parse dates to datetime, sort by amfi_code + date, forward-fill missing NAV for holidays/weekends, remove duplicates, validate NAV > 0.
Clean investor_transactions.csv — standardise transaction_type values (SIP/Lumpsum/Redemption), validate amount > 0, fix date formats, check KYC status enum values.
Clean scheme_performance.csv — validate all return values are numeric, flag anomalies, check expense_ratio range (0.1% – 2.5%).
Design SQLite star schema — write CREATE TABLE statements for dim_fund, dim_date, fact_nav, fact_transactions, fact_performance, fact_aum. Define primary and foreign keys.
Load all cleaned datasets into SQLite — use SQLAlchemy create_engine + df.to_sql(). Verify row counts match source CSVs.
Write 10 analytical SQL queries — top 5 funds by AUM, average NAV per month, SIP YoY growth, transactions by state, funds with expense_ratio < 1%, and 5 more of your choice.
Create data dictionary — document all columns, data types, business definitions, and source references in a Markdown file.
Git commit: "Day 2: Cleaned data + SQLite DB loaded"
Deliverables: 10 cleaned CSVs in data/processed/, bluestock_mf.db, schema.sql, queries.sql, data_dictionary.md

task3:
Exploratory Data Analysis (EDA)
TODO
TASK
MEDIUM
Assigned to
MY
mythiliseenivasan11
SH
shivamshrivastavadeepspace
TE
tejaswibhardwaj13
AB
abhishek.kumar529127
KS
Karan Veer Singh
Due : 11 Jun 2026
Time estimate: 7–8 hours

Tasks:

NAV trend analysis — plot daily NAV for all 40 schemes 2022–2026. Highlight 2023 bull run and 2024 market corrections using Plotly.
AUM growth bar chart — grouped bar by fund house for each year 2022–2025. Highlight SBI at ₹12.5L Cr dominance using Seaborn.
SIP inflow time-series — monthly SIP trend Jan 2022 – Dec 2025. Annotate the ₹31,002 Cr all-time high (Dec 2025) using Plotly.
Category inflow heatmap — months on X-axis, fund categories on Y-axis, net inflow as colour intensity using Seaborn.
Investor demographics — age group distribution pie chart. SIP amount box plot by age group. Gender split.
Geographic distribution — horizontal bar chart of SIP amount by state. T30 vs B30 city tier pie chart.
Folio count growth — line chart from 13.26 Cr (Jan 2022) to 26.12 Cr (Dec 2025). Mark key milestones.
NAV return correlation matrix — compute pairwise correlation of daily returns for 10 selected funds. Seaborn heatmap.
Sector allocation donut — aggregate sector weights from portfolio_holdings.csv across all equity funds.
Document 10 key EDA findings in Jupyter Markdown cells — each = 1 insight sentence + supporting chart reference.
Deliverables: EDA_Analysis.ipynb with 15+ charts, exported PNG charts for final report

task 4:
Fund Performance Analytics
TODO
TASK
MEDIUM
Assigned to
MY
mythiliseenivasan11
SH
shivamshrivastavadeepspace
TE
tejaswibhardwaj13
AB
abhishek.kumar529127
KS
Karan Veer Singh
Due : 13 Jun 2026
Time estimate: 7–8 hours

Tasks:

Compute daily returns — daily_return = nav_t / nav_t-1 − 1 for all 40 schemes. Validate distribution looks reasonable.
Compute CAGR for 1yr, 3yr, 5yr — CAGR = (NAV_end / NAV_start) ^ (1/n) − 1. Build a comparison table across all funds.
Sharpe Ratio — (Rp − Rf) / Std(Rp) × √252. Use Rf = 6.5% (RBI repo rate proxy). Rank all 40 funds.
Sortino Ratio — same formula but denominator uses only downside standard deviation (negative return days only).
Alpha and Beta — OLS regression of fund returns on Nifty 100 returns using scipy.stats.linregress. Alpha = intercept × 252.
Maximum Drawdown — min(NAV / running_max − 1) for each fund. Find worst drawdown date range.
Fund Scorecard (0–100) — composite: 30% × 3yr return rank + 25% × Sharpe rank + 20% × Alpha rank + 15% × expense ratio rank (inverse) + 10% × max DD rank (inverse).
Benchmark comparison chart — plot top 5 funds vs Nifty 50 and Nifty 100 over 3 years. Compute tracking error = std(fund_return − benchmark_return) × √252.
Deliverables: Performance_Analytics.ipynb, fund_scorecard.csv, alpha_beta.csv, benchmark comparison chart PNG

task 5:
Dashboard Development (Power BI / Tableau)
TODO
TASK
MEDIUM
Assigned to
MY
mythiliseenivasan11
SH
shivamshrivastavadeepspace
TE
tejaswibhardwaj13
AB
abhishek.kumar529127
KS
Karan Veer Singh
Due : 16 Jun 2026
Time estimate: 7–8 hours

Tasks:

Connect Power BI to data — import all cleaned CSVs or connect via SQLite ODBC. Verify all 8 tables load. Create relationships on amfi_code and date.
Page 1 — Industry Overview — KPI cards: Total AUM (₹81L Cr), SIP Inflows (₹31K Cr), Folios (26.12 Cr), Schemes (1,908). Line chart: industry AUM trend 2022–2025. Bar chart: AUM by AMC.
Page 2 — Fund Performance — Scatter plot: return (X) vs risk/StdDev (Y), bubble size = AUM. Sortable fund scorecard table. NAV line vs benchmark. Slicers: fund house, category, plan.
Page 3 — Investor Analytics — Bar chart: transaction amount by state. Donut: SIP/Lumpsum/Redemption split. Bar: age group vs avg SIP amount. Monthly transaction volume line. Slicers: state, age group, city tier.
Page 4 — SIP & Market Trends — Dual-axis: SIP inflow (bar) + Nifty 50 (line) 2022–2025. Category inflow heatmap. Top 5 categories by net inflow FY25.
Add interactivity — drill-through from fund table to NAV detail page. Tooltips on all charts. Apply Bluestock colour theme and logo.
Export — save as .pbix. Export to PDF. Export each page as PNG for the final report.
Deliverables: bluestock_mf_dashboard.pbix, Dashboard.pdf, 4 page PNG screenshots

task 6:
Advanced Analytics + Risk Metrics
TODO
TASK
MEDIUM
Assigned to
MY
mythiliseenivasan11
SH
shivamshrivastavadeepspace
TE
tejaswibhardwaj13
AB
abhishek.kumar529127
KS
Karan Veer Singh
Due : 18 Jun 2026
Time estimate: 6–7 hours

Tasks:

Historical VaR (95%) — 5th percentile of daily return distribution. CVaR = mean of returns below VaR threshold. Compute for all 40 schemes.
Rolling 90-day Sharpe — returns.rolling(90).mean() / returns.rolling(90).std() × √252. Plot over time for 5 key funds.
Investor cohort analysis — group by first transaction year. Compute avg SIP amount, total invested, and top fund preference per cohort.
SIP continuity analysis — for investors with 6+ SIP transactions, compute avg gap between dates. Flag investors with gap > 35 days as "at-risk".
Simple fund recommender — input: risk appetite (Low / Moderate / High). Output: top 3 funds by Sharpe ratio within matching risk_grade. Print recommendation table.
Sector HHI concentration — Herfindahl-Hirschman Index = Σ(weight_i²) per fund. High HHI = concentrated portfolio. Compare across all equity funds.
Write 5 advanced insights in Jupyter Markdown — which funds have highest VaR, which investor cohorts invest most, SIP continuity rate, etc.
Deliverables: Advanced_Analytics.ipynb, var_cvar_report.csv, recommender.py, rolling_sharpe_chart.png

task 7:
Final Report + Presentation + Deployment
TODO
TASK
MEDIUM
Assigned to
MY
mythiliseenivasan11
SH
shivamshrivastavadeepspace
TE
tejaswibhardwaj13
AB
abhishek.kumar529127
KS
Karan Veer Singh
Due : 21 Jun 2026
Time estimate: 6–7 hours

Tasks:

Write final PDF report — sections: executive summary, data sources, ETL design, EDA findings, performance analysis, dashboard screenshots, limitations, recommendations. Target 15–20 pages.
Create 12-slide presentation — title, problem & objective, data sources, architecture, EDA highlights (×2), performance metrics (×2), dashboard screenshots (×2), key findings, thank you.
Clean all Python scripts — add docstrings, remove debug prints, create run_pipeline.py as master execution script.
Write README.md — project overview, setup instructions, how to run the ETL, how to open the dashboard, dataset descriptions.
Final GitHub push + tag — git add . && git commit -m "Final: Complete Bluestock MF Capstone" && git tag v1.0 && git push
(Optional) Publish dashboard — Power BI Service (free account) or Tableau Public. Add URL to README.
Self-review checklist — all 8 objectives met? All 7 deliverables submitted? Code runs without errors? Dashboard loads? Report is professional?
Deliverables: Final_Report.pdf (15–20 pages), Bluestock_MF_Presentation.pptx (12 slides), clean GitHub repo with README + v1.0 tag

task8:
DELIVERABLES & EVALUATION RUBRIC
TODO
TASK
MEDIUM
Assigned to
MY
mythiliseenivasan11
SH
shivamshrivastavadeepspace
TE
tejaswibhardwaj13
AB
abhishek.kumar529127
KS
Karan Veer Singh
Due : 22 Jun 2026
IDDeliverableFormatWeightCriteriaD1ETL pipeline script.py15%Runs without manual steps, error handling, clean codeD2SQLite database.db10%Correct schema, all data loaded, queries runD3EDA notebook.ipynb15%Depth of analysis, chart quality, insights documentedD4Performance metrics.ipynb + CSVs15%Mathematical accuracy, correct Sharpe/Beta/VaR formulasD5Interactive dashboard.pbix or .twbx20%Design quality, all 4 pages, slicers functionalD6Advanced analytics.ipynb10%VaR correctness, cohort analysis quality, recommender logicD7Final report + slides.pdf + .pptx15%Professional quality, complete sections, clear findings

BONUS CHALLENGES (+10 marks each)
B1 — Schedule ETL as a cron job auto-fetching NAV from mfapi.in every weekday at 8 PM
B2 — Build a Streamlit web app as an alternative to Power BI
B3 — Monte Carlo simulation projecting NAV growth over 5 years with uncertainty bands
B4 — Markowitz Efficient Frontier portfolio optimisation for 5 selected funds
B5 — Automated HTML email report generator sending weekly performance summaries
COMMON MISTAKES TO AVOID
❌ Hard-coding file paths — use pathlib.Path or os.path.join
❌ Not handling weekends/holidays in NAV — always ffill() after reindexing to full date range
❌ Using calendar days for CAGR — annualise with 252 / n_trading_days
❌ Dashboard with no slicers — every page needs at least 2 interactive filters
❌ Confusing AUM lakh crore with scheme-level AUM crore — include units in column names
❌ Committing .db files to GitHub — add *.db to .gitignore, share schema.sql instead
FOLDER STRUCTURE




bluestock_mf_capstone/
├── data/
│   ├── raw/           ← original downloaded files
│   ├── processed/     ← cleaned, merged CSVs
│   └── db/            ← bluestock_mf.db (SQLite)
├── notebooks/
│   ├── 01_data_ingestion.ipynb
│   ├── 02_data_cleaning.ipynb
│   ├── 03_eda_analysis.ipynb
│   ├── 04_performance_analytics.ipynb
│   └── 05_advanced_analytics.ipynb
├── scripts/
│   ├── etl_pipeline.py
│   ├── live_nav_fetch.py
│   ├── compute_metrics.py
│   └── recommender.py
├── sql/
│   ├── schema.sql
│   └── queries.sql
├── dashboard/
│   └── bluestock_mf.pbix
├── reports/
│   ├── Final_Report.pdf
│   └── Presentation.pptx
└── README.md


additional context:
after every task is completed, i need you to push the changes to github, make sure the code is clean and well-documented.

after evert task is done, if there is some task which is cant be done by you or needs user attention or action on some other platform or something, update this intruction,md and alert the user in the chat screen

for the pdf adn slide, creat md files in the reports folder as the said directory of the project and write the content in detail and elaborated form with formatting, like for ppt slides mention slide 1 2 3 4 etc, and content inside professional harvard level MBA sharp and smart yet human made and dont useem dash anywhere. for pdf make it with page number formatting, heading subheading etc mention so its easy to format it for the user.

for addtional context of the project read projectfile.md, it is the project file with elaborate details of the porject as its a readymade file and we will adhere to its tech and specs and may some modifications if we improve upon the project without killing the requirnments and funtionality

the code style do not use em dash anywhere, keep comments small and concise adn humar written, simple and easy. just concise enough and lazy like to let a auditor know its use.

strictly stick to this file formatting at the initialisation itself

bluestock_mf_capstone/
├── data/
│   ├── raw/           ← original downloaded files
│   ├── processed/     ← cleaned, merged CSVs
│   └── db/            ← bluestock_mf.db (SQLite)
├── notebooks/
│   ├── 01_data_ingestion.ipynb
│   ├── 02_data_cleaning.ipynb
│   ├── 03_eda_analysis.ipynb
│   ├── 04_performance_analytics.ipynb
│   └── 05_advanced_analytics.ipynb
├── scripts/
│   ├── etl_pipeline.py
│   ├── live_nav_fetch.py
│   ├── compute_metrics.py
│   └── recommender.py
├── sql/
│   ├── schema.sql
│   └── queries.sql
├── dashboard/
│   └── bluestock_mf.pbix
├── reports/
│   ├── Final_Report.pdf
│   └── Presentation.pptx
└── README.md

without being asked, after every task completion when you are satisfied, do a thorough verification adn validation of the task, testing and error checking of logic, concept, syntax, workflow, directory and more and everything, after that run the said stuff hypotheticcaly or actually line by line tto find more error and bugs, leave no stones unturned, make it sharp and smart. and test like a senior developr with all the experience in the world, and once all done and set that yeah its done, update the github repo and push it to the main branch and also create a tag v1.0 and push it to the main branch and then alert the user.