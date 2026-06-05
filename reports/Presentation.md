# Bluestock Mutual Funds Analytics Platform
### Capstone Presentation Content

--------------------------------------------------
## SLIDE 1: Title Slide
**Title:** Bluestock Mutual Funds Analytics: A Comprehensive Data Platform
**Subtitle:** End-to-End ETL, Quantitative Modeling, and Interactive Visualization
**Presenter:** Karan Veer Singh
**Links:** [LinkedIn Profile](https://www.linkedin.com/in/karanveersingh05/) | [GitHub Repository](https://github.com/karanveersingh05/MutualFundsAnalytics)

--------------------------------------------------
## SLIDE 2: Executive Summary
**Key Message:** Transforming raw financial data into actionable investment intelligence.
*   **The Challenge:** Retail investors lack institutional-grade analytics to evaluate Indian mutual funds.
*   **The Solution:** An automated ETL pipeline and interactive dashboard offering deep risk-return analysis.
*   **Key Capabilities:** 
    *   Automated daily NAV ingestion via AMFI.
    *   Factor-weighted scoring models (Alpha, Sharpe, Drawdown).
    *   Advanced quantitative projections (Monte Carlo, Markowitz).
*   **Business Impact:** Empowers data-driven portfolio allocation and identifies at-risk investor segments.

--------------------------------------------------
## SLIDE 3: The Market Opportunity
**Key Message:** The Indian Mutual Fund industry is experiencing exponential growth, demanding sophisticated tracking.
*   **AUM Surge:** Industry AUM has crossed massive milestones, driven by retail participation.
*   **The SIP Revolution:** Systematic Investment Plans (SIP) form the backbone of retail inflows.
*   **Data Fragmentation:** Despite the growth, performance data remains scattered across multiple AMC domains and regulatory bodies.
*   **Need for Centralization:** A unified data warehouse is critical for comparative analysis across 40+ bluechip and midcap schemes.

--------------------------------------------------
## SLIDE 4: Architecture & Technology Stack
**Key Message:** A robust, automated, and scalable Python-based data infrastructure.
*   **Languages & Core:** Python, SQL
*   **ETL & Processing:** Pandas, NumPy, SQLite3, Schedule
*   **Visualization:** Plotly, Seaborn, Matplotlib, Streamlit
*   **Automation:** Windows Batch scripting, Smtplib (HTML Emails)

```mermaid
graph TD
    A[AMFI API / Raw CSVs] -->|Extract| B(Data Ingestion)
    B -->|Clean & Transform| C(Pandas Processing)
    C -->|Load| D[(SQLite Data Warehouse)]
    D -->|Query| E[Quantitative Models]
    D -->|Query| F[Streamlit Web App]
    E --> G[Automated HTML Emails]
    E --> H[Chart Artifacts]
```

--------------------------------------------------
## SLIDE 5: Data Modeling & Schema
**Key Message:** A normalized Star Schema designed for high-performance analytical queries.

```mermaid
erDiagram
    DIM_FUND ||--o{ FACT_NAV : tracks
    DIM_FUND ||--o{ FACT_PERFORMANCE : evaluates
    DIM_FUND ||--o{ FACT_TRANSACTIONS : receives
    DIM_FUND {
        int amfi_code PK
        string scheme_name
        string category
        string risk_grade
    }
    FACT_NAV {
        int amfi_code FK
        date date
        float nav
    }
    FACT_TRANSACTIONS {
        string investor_id
        int amfi_code FK
        float amount_inr
    }
```

--------------------------------------------------
## SLIDE 6: Core Analytics - Risk vs. Return
**Key Message:** Moving beyond simple CAGR to true risk-adjusted performance evaluation.
*   **Sharpe Ratio Calculation:** Measuring excess return per unit of volatility.
*   **Alpha & Beta:** Tracking fund manager skill against benchmark indices (Nifty 50, Nifty Midcap 150).
*   **Maximum Drawdown:** Stress-testing funds by evaluating historical peak-to-trough declines.
*   **The Bluestock Composite Score:** A proprietary 0-100 ranking system weighting returns against expense ratios and risk metrics.

--------------------------------------------------
## SLIDE 7: Investor Behavioral Analytics
**Key Message:** Decoding retail transaction patterns to optimize client retention.
*   **Geographic Distribution:** Identifying high-growth Tier 2 and Tier 3 cities driving AUM expansion.
*   **Cohort Analysis:** Grouping investors by acquisition year to track lifetime value and average ticket size.
*   **SIP Continuity Flagging:** 
    *   Algorithmic detection of "at-risk" investors.
    *   Flags accounts with inter-transaction gaps exceeding 35 days.

--------------------------------------------------
## SLIDE 8: Advanced Modeling - Monte Carlo Simulations
**Key Message:** Projecting future NAVs utilizing Geometric Brownian Motion.
*   **Methodology:** 
    *   Extracted historical daily log returns, drift, and volatility.
    *   Simulated 1,000 unique market paths spanning 1,260 trading days (5 years).
*   **Outputs:** 
    *   Uncertainty bands at the 5th, 50th, and 95th percentiles.
    *   Allows risk-averse investors to visualize "worst-case" scenario baselines.

--------------------------------------------------
## SLIDE 9: Modern Portfolio Theory (Markowitz)
**Key Message:** Mathematically optimizing asset allocation across a diversified basket of funds.
*   **The Approach:** Simulated 10,000 distinct portfolio weightings across Large Cap, Mid Cap, Small Cap, and Debt funds.
*   **Efficient Frontier Construction:** Plotted Expected Risk against Expected Return.
*   **Key Deliverables:** 
    *   Identified the absolute **Maximum Sharpe Ratio** portfolio.
    *   Identified the **Minimum Volatility** portfolio for conservative clients.

--------------------------------------------------
## SLIDE 10: The Streamlit Interactive Dashboard
**Key Message:** Delivering the analytics engine directly to the user through a premium interface.
*   **Apple-Inspired Aesthetics:** Clean layout, Sans-Serif typography, and minimalist metrics.
*   **Dynamic Filtering:** Real-time cross-filtering by AMC and Fund Category.
*   **Key Modules:** 
    *   Macro Industry Overview
    *   Fund Performance Scatter Plots
    *   Investor Demographics Breakdown
    *   Systematic Investment (SIP) Trends

--------------------------------------------------
## SLIDE 11: Pipeline Automation & Reporting
**Key Message:** A zero-touch operational ecosystem.
*   **Daemonized Scheduling:** ETL pipeline programmed to auto-execute via Python schedulers.
*   **HTML Email Engine:** 
    *   Automatically parses the top 5 funds from the newest Composite Scorecard.
    *   Generates a styled HTML newsletter.
    *   Transmits silently via SMTP for weekly stakeholder updates.

--------------------------------------------------
## SLIDE 12: Business Value & Strategic Impact
**Key Message:** How this platform serves stakeholders.
*   **For Retail Investors:** Democratizes access to institutional metrics like Alpha, Beta, and Efficient Frontiers.
*   **For AMCs / Brokers:** Predicts churn via SIP continuity analysis and highlights geographic hotspots.
*   **For Fund Analysts:** Fully automates the tedious daily task of NAV data cleaning and benchmark alignment.

--------------------------------------------------
## SLIDE 13: Technical Challenges Conquered
**Key Message:** Overcoming real-world data engineering hurdles.
*   **Missing Weekend NAVs:** Solved using forward-fill algorithms to ensure accurate daily compounding.
*   **Column Naming Collisions:** Resolved `_x` and `_y` merge conflicts through strict schema definitions.
*   **Headless Matplotlib Generation:** Engineered the pipeline to use non-interactive backends to prevent GUI crashes during automated cron execution.

--------------------------------------------------
## SLIDE 14: Conclusion & Future Scope
**Key Message:** A highly capable V1 platform with room to scale.
*   **Current State:** A fully functioning, end-to-end Python financial data product.
*   **Future Scope:** 
    *   Cloud migration (AWS RDS for database, Lambda for ETL).
    *   Integration of predictive Machine Learning models for NAV forecasting.
    *   Live order execution APIs via broker gateways.

--------------------------------------------------
## SLIDE 15: Q&A
**Title:** Thank You
*   **Developer:** Karan Veer Singh
*   **Repository:** [github.com/karanveersingh05/MutualFundsAnalytics](https://github.com/karanveersingh05/MutualFundsAnalytics)
*   **LinkedIn:** [linkedin.com/in/karanveersingh05](https://www.linkedin.com/in/karanveersingh05/)
*   **Open for Questions.**
