"""
streamlit_app.py
Bluestock Mutual Fund Analytics Platform - Streamlit Web App
"""
import sys
import smtplib
import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

import streamlit as st
import pandas as pd
import plotly.express as px

# --- Page Config ---
st.set_page_config(page_title="BlueStock MF Analytics", layout="wide", initial_sidebar_state="expanded")

# --- Custom Apple-like CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    .stApp {
        background-color: #F5F5F7;
        color: #1D1D1F;
    }

    h1, h2, h3, h4, h5, h6 {
        font-weight: 600;
        letter-spacing: -0.02em;
        color: #1D1D1F !important;
    }

    div[data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid #E5E5EA;
    }

    div[data-testid="stMetricValue"] {
        font-size: 2.2rem !important;
        font-weight: 600;
        color: #1D1D1F;
    }

    div[data-testid="stMetricLabel"] {
        font-size: 0.85rem !important;
        font-weight: 500;
        color: #86868B;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    div[data-testid="stMetricDelta"] {
        font-weight: 500;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }

    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid #E5E5EA;
    }
    </style>
""", unsafe_allow_html=True)

# Shared Plotly Theme
plotly_layout = dict(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(family="Inter, -apple-system, sans-serif", color="#1D1D1F"),
    margin=dict(l=20, r=20, t=40, b=20),
)

# Base directory for absolute path resolution
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / 'data' / 'processed'
SCRIPTS_DIR = BASE_DIR / 'scripts'

# --- Data Loading ---
@st.cache_data
def load_data():
    data = {}
    try:
        data['fund_master'] = pd.read_csv(DATA_DIR / '01_fund_master_clean.csv')
        data['aum'] = pd.read_csv(DATA_DIR / '03_aum_by_fund_house_clean.csv')
        data['sip'] = pd.read_csv(DATA_DIR / '04_monthly_sip_inflows_clean.csv')
        data['category_inflows'] = pd.read_csv(DATA_DIR / '05_category_inflows_clean.csv')
        data['scorecard'] = pd.read_csv(DATA_DIR / 'fund_scorecard.csv')
        data['transactions'] = pd.read_csv(DATA_DIR / '08_investor_transactions_clean.csv')
        data['mc_summary'] = pd.read_csv(DATA_DIR / 'monte_carlo_summary.csv')
        data['optimal_portfolio'] = pd.read_csv(DATA_DIR / 'optimal_portfolio.csv')
    except Exception as e:
        st.error(f"Data load error: {e}")
    return data

data = load_data()

# --- Sidebar ---
st.sidebar.markdown("""
<div style='padding: 10px 0 5px 0;'>
    <div style='font-size:1.6rem; font-weight:700; line-height:1.2; color:#1D1D1F;'>
        BlueStock<br>Mutual Funds<br>Analytics
    </div>
    <div style='margin-top:10px; font-size:0.82rem; color:#86868B;'>
        Made by <a href='https://www.linkedin.com/in/karanveersingh05/'
        target='_blank'
        style='color:#007AFF; text-decoration:none; font-weight:500;'>Karan Veer Singh</a>
    </div>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")
page = st.sidebar.radio("Navigation", [
    "Industry Overview",
    "Fund Performance",
    "Investor Analytics",
    "SIP Trends",
    "Monte Carlo Simulation",
    "Portfolio Optimization",
    "About Project"
])
st.sidebar.markdown("---")
st.sidebar.caption("v1.7 | Bluestock MF Capstone")

if not data:
    st.stop()

# =============================================================================
# Page 1: Industry Overview
# =============================================================================
if page == "Industry Overview":
    st.title("Industry Overview")
    st.markdown("Macro-level view of the Indian Mutual Fund Industry.")
    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Industry AUM", "₹81.0 L Cr", "+1.2%")
    with col2:
        st.metric("SIP Inflows (Dec '25)", "₹31,002 Cr", "+4.5%")
    with col3:
        st.metric("Total Folios", "26.12 Cr", "+2.1%")
    with col4:
        st.metric("Total Schemes", "1,908")

    st.markdown("<br><hr style='border:1px solid #E5E5EA'><br>", unsafe_allow_html=True)

    col_a, col_b = st.columns([2, 1])

    with col_a:
        st.subheader("Top Fund Houses by AUM")
        if 'aum' in data:
            latest_aum = (data['aum'].groupby('fund_house')['aum_crore']
                          .max().reset_index()
                          .sort_values('aum_crore', ascending=False).head(10))
            fig = px.bar(latest_aum, x='fund_house', y='aum_crore',
                         color='fund_house',
                         color_discrete_sequence=px.colors.qualitative.Pastel)
            fig.update_layout(**plotly_layout, showlegend=False,
                              xaxis_title="", yaxis_title="AUM (Cr)")
            st.plotly_chart(fig, use_container_width=True)

    with col_b:
        st.subheader("Category Net Inflows (FY25)")
        if 'category_inflows' in data:
            cat_sum = (data['category_inflows'].groupby('category')['net_inflow_crore']
                       .sum().reset_index())
            fig = px.pie(cat_sum, names='category', values='net_inflow_crore', hole=0.6,
                         color_discrete_sequence=px.colors.qualitative.Set2)
            fig.update_layout(**plotly_layout, showlegend=False)
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)

# =============================================================================
# Page 2: Fund Performance
# =============================================================================
elif page == "Fund Performance":
    st.title("Fund Performance & Risk")
    st.markdown("Compare risk-adjusted returns across the Bluestock universe.")
    st.markdown("<br>", unsafe_allow_html=True)

    if 'scorecard' in data and 'fund_master' in data:
        df_score = pd.merge(
            data['scorecard'],
            data['fund_master'][['amfi_code', 'fund_house', 'category']],
            on='amfi_code', how='left'
        )

        col1, col2 = st.columns(2)
        with col1:
            amc_list = ["All"] + sorted(df_score['fund_house'].dropna().unique().tolist())
            amc_filter = st.selectbox("Select AMC", amc_list)
        with col2:
            cat_list = ["All"] + sorted(df_score['category'].dropna().unique().tolist())
            cat_filter = st.selectbox("Select Category", cat_list)

        filtered_df = df_score.copy()
        if amc_filter != "All":
            filtered_df = filtered_df[filtered_df['fund_house'] == amc_filter]
        if cat_filter != "All":
            filtered_df = filtered_df[filtered_df['category'] == cat_filter]

        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("Risk vs Return")

        # Guard: need at least 1 row and non-null scorecard scores to plot bubble size
        plot_df = filtered_df.dropna(subset=['cagr_3y', 'alpha', 'scorecard_0_100'])
        if not plot_df.empty:
            fig = px.scatter(plot_df, x='cagr_3y', y='alpha',
                             size='scorecard_0_100', color='category',
                             hover_name='scheme_name',
                             labels={'cagr_3y': '3Y CAGR', 'alpha': 'Alpha'},
                             color_discrete_sequence=px.colors.qualitative.Bold)
            fig.update_layout(**plotly_layout)
            fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#E5E5EA')
            fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#E5E5EA')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No data available for the selected filters.")

        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("Fund Scorecard Ranking")

        display_df = filtered_df[['scheme_name', 'fund_house', 'category',
                                   'scorecard_0_100', 'cagr_3y', 'sharpe', 'alpha']].copy()
        display_df.columns = ['Scheme Name', 'AMC', 'Category', 'Score (0-100)',
                               '3Y CAGR', 'Sharpe', 'Alpha']
        display_df = display_df.sort_values('Score (0-100)', ascending=False).reset_index(drop=True)
        st.dataframe(display_df, use_container_width=True)

# =============================================================================
# Page 3: Investor Analytics
# =============================================================================
elif page == "Investor Analytics":
    st.title("Investor Analytics")
    st.markdown("Insights into investor behaviour, geography, and transaction types.")
    st.markdown("<br>", unsafe_allow_html=True)

    if 'transactions' in data:
        tx = data['transactions']

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Transaction Type Split")
            tx_type = tx['transaction_type'].value_counts().reset_index()
            tx_type.columns = ['Type', 'Count']
            fig = px.pie(tx_type, names='Type', values='Count', hole=0.5,
                         color_discrete_sequence=['#34C759', '#007AFF', '#FF3B30'])
            fig.update_layout(**plotly_layout)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.subheader("City Tier Distribution")
            tier = tx['city_tier'].value_counts().reset_index()
            tier.columns = ['Tier', 'Count']
            fig = px.bar(tier, x='Tier', y='Count', color='Tier',
                         color_discrete_sequence=['#5856D6', '#FF9500', '#34C759'])
            fig.update_layout(**plotly_layout, showlegend=False, xaxis_title="")
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("<br><hr style='border:1px solid #E5E5EA'><br>", unsafe_allow_html=True)
        st.subheader("Transactions by State")
        state_sum = (tx.groupby('state')['amount_inr'].sum()
                     .reset_index().sort_values('amount_inr', ascending=False))
        fig = px.bar(state_sum, x='amount_inr', y='state', orientation='h',
                     color='amount_inr', color_continuous_scale='Blues')
        fig.update_layout(**plotly_layout,
                          yaxis={'categoryorder': 'total ascending'},
                          yaxis_title="", xaxis_title="Total Amount ()")
        st.plotly_chart(fig, use_container_width=True)

# =============================================================================
# Page 4: SIP Trends
# =============================================================================
elif page == "SIP Trends":
    st.title("SIP & Market Trends")
    st.markdown("Analysing the phenomenal growth of systematic investing in India.")
    st.markdown("<br>", unsafe_allow_html=True)

    if 'sip' in data:
        sip = data['sip'].copy()

        st.subheader("Monthly SIP Inflows Growth")
        fig = px.area(sip, x='month', y='sip_inflow_crore',
                      labels={'month': 'Month', 'sip_inflow_crore': 'Inflow ( Cr)'},
                      color_discrete_sequence=['#34C759'])
        fig.update_layout(**plotly_layout)
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#E5E5EA')
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#E5E5EA')
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("Active SIP Accounts")
        fig2 = px.line(sip, x='month', y='active_sip_accounts_crore', markers=True,
                       labels={'month': 'Month', 'active_sip_accounts_crore': 'Active Accounts (Cr)'},
                       color_discrete_sequence=['#007AFF'])
        fig2.update_layout(**plotly_layout)
        fig2.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#E5E5EA')
        fig2.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#E5E5EA')
        st.plotly_chart(fig2, use_container_width=True)

# =============================================================================
# Page 5: Monte Carlo Simulation (Task 11)
# =============================================================================
elif page == "Monte Carlo Simulation":
    st.title("Monte Carlo NAV Projections")
    st.markdown("5-year projected NAV growth with uncertainty bands (1,000 simulations per fund).")
    st.markdown("<br>", unsafe_allow_html=True)

    if 'mc_summary' in data:
        st.subheader("5-Year Projection Summary")
        st.dataframe(data['mc_summary'], use_container_width=True)

    chart_path = BASE_DIR / 'reports' / 'charts' / 'monte_carlo_bands.png'
    if chart_path.exists():
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("Simulation Chart")
        st.image(str(chart_path), caption="Monte Carlo NAV Bands (5th / 50th / 95th percentile)", use_container_width=True)
    else:
        st.warning("Chart not found. Please run the pipeline first via run.bat.")

# =============================================================================
# Page 6: Portfolio Optimization (Task 12)
# =============================================================================
elif page == "Portfolio Optimization":
    st.title("Markowitz Efficient Frontier")
    st.markdown("Optimal asset allocation using Modern Portfolio Theory (10,000 simulated portfolios).")
    st.markdown("<br>", unsafe_allow_html=True)

    if 'optimal_portfolio' in data:
        df_opt = data['optimal_portfolio']
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Max Sharpe Ratio Portfolio")
            sharpe_df = df_opt[['scheme_name', 'max_sharpe_weight_pct']].copy()
            sharpe_df.columns = ['Scheme Name', 'Allocation (%)']
            fig = px.pie(sharpe_df, names='Scheme Name', values='Allocation (%)',
                         hole=0.5, color_discrete_sequence=px.colors.qualitative.Bold)
            fig.update_layout(**plotly_layout, showlegend=False)
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.subheader("Min Volatility Portfolio")
            vol_df = df_opt[['scheme_name', 'min_volatility_weight_pct']].copy()
            vol_df.columns = ['Scheme Name', 'Allocation (%)']
            fig = px.pie(vol_df, names='Scheme Name', values='Allocation (%)',
                         hole=0.5, color_discrete_sequence=px.colors.qualitative.Pastel)
            fig.update_layout(**plotly_layout, showlegend=False)
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("Optimal Weight Comparison")
        st.dataframe(df_opt, use_container_width=True)

    chart_path = BASE_DIR / 'reports' / 'charts' / 'efficient_frontier.png'
    if chart_path.exists():
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("Efficient Frontier Chart")
        st.image(str(chart_path), caption="Efficient Frontier: Each dot = one simulated portfolio", use_container_width=True)
    else:
        st.warning("Chart not found. Please run the pipeline first via run.bat.")

# =============================================================================
# Page 7: About Project
# =============================================================================
elif page == "About Project":
    st.title("About the Project")
    st.markdown("A deep dive into the architecture, datasets, and quantitative models powering the **Bluestock Mutual Funds Analytics** platform.")
    st.markdown("<br>", unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["Architecture & ETL", "Datasets & Schema", "Quantitative Models", "Tech Stack"])
    
    with tab1:
        st.subheader("End-to-End Data Pipeline")
        st.markdown("""
        The platform operates on a fully automated, 'zero-touch' Python ETL pipeline. 
        
        **1. Extraction (Ingestion)**
        - Ingests **10 raw historical CSVs** containing transaction data, historical NAVs, and fund metadata.
        - Interfaces with the **Live AMFI API** to download the absolute latest Net Asset Values (NAV) for top tracking funds dynamically.
        
        **2. Transformation (Cleaning)**
        - **Temporal Alignment:** Financial data is inherently messy due to weekends and public holidays. The pipeline reindexes all dates to a complete calendar and utilizes algorithmic **forward-filling (ffill)** to ensure compounding calculations are perfectly accurate.
        - **Outlier Mitigation:** Regulatory ceilings are applied. For example, any expense ratio exceeding SEBI's 2.5% cap is mathematically clipped to prevent scoring anomalies.
        
        **3. Loading (Warehouse)**
        - The transformed data is pushed into a local **SQLite** database, strictly modeled as a high-performance **Star Schema**.
        """)
        
        with st.expander("View Pipeline Script Execution Order"):
            st.code('''
            1. live_nav_fetch.py
            2. data_ingestion.py
            3. data_cleaning.py
            4. run_eda.py
            5. compute_metrics.py
            6. generate_advanced_analytics.py
            7. monte_carlo_simulation.py
            8. markowitz_optimization.py
            9. email_report_generator.py
            ''', language='text')

    with tab2:
        st.subheader("Data Modeling")
        st.markdown("""
        The core relational database (`bluestock_mf.db`) utilizes a **Star Schema** to separate static dimensions from rapidly growing transactional facts.
        """)
        
        col1, col2 = st.columns(2)
        with col1:
            st.info("**Dimension Tables**")
            st.markdown("""
            - `dim_fund`: Fund metadata (AMC, Category, Expense Ratio).
            - `dim_date`: Complete calendar mapped to quarters and weekends.
            """)
        with col2:
            st.success("**Fact Tables**")
            st.markdown("""
            - `fact_nav`: 64,000+ daily NAV records.
            - `fact_transactions`: 32,000+ retail investor records.
            - `fact_performance`: Calculated Sharpe, Alpha, and composite scores.
            """)
            
        st.markdown("---")
        st.markdown("**The 10 Core Raw Datasets:**")
        st.markdown("""
        1. `01_fund_master.csv` - Reference table: fund house, category, risk grade
        2. `02_nav_history.csv` - Daily NAV for 40 schemes (2022-2026)
        3. `03_aum_by_fund_house.csv` - Quarterly AUM by AMC
        4. `04_monthly_sip_inflows.csv` - Industry SIP inflow data
        5. `05_category_inflows.csv` - Net fund category inflows by month
        6. `06_industry_folio_count.csv` - Total folios, equity/debt/hybrid split
        7. `07_scheme_performance.csv` - Return metrics, Sharpe, Sortino, Alpha, Beta
        8. `08_investor_transactions.csv` - 32K+ investor SIP/Lumpsum records
        9. `09_portfolio_holdings.csv` - Stock-level portfolio weights per fund
        10. `10_benchmark_indices.csv` - Nifty 50, Nifty 100 benchmark data
        """)

    with tab3:
        st.subheader("Financial Mathematics & Analytics")
        st.markdown("The platform leverages institutional-grade models rather than simple absolute returns.")
        
        st.markdown("**Core Performance Metrics:**")
        st.markdown("""
        - **Sharpe Ratio:** Measures risk-adjusted return (Excess Return / Volatility).
        - **Sortino Ratio:** Similar to Sharpe, but only penalizes *downside* volatility.
        - **Alpha & Beta:** Evaluates a fund manager's ability to beat the benchmark index (Nifty 50).
        - **Maximum Drawdown:** Stress-tests funds by calculating the largest historical peak-to-trough drop.
        """)
        
        st.markdown("**Behavioral & Structural Analytics:**")
        st.markdown("""
        - **SIP Continuity Engine:** Scans transaction histories to flag investors whose inter-transaction gaps exceed 35 days (predictive churn analysis).
        - **Cohort Analysis:** Groups investors by acquisition year to map Lifetime Value (LTV) and average transaction sizes.
        - **Herfindahl-Hirschman Index (HHI):** Applies macroeconomic concentration mathematics to portfolio holdings to identify funds over-exposed to a single stock.
        """)
        
        st.markdown("**Advanced Quantitative Models:**")
        with st.expander("1. Monte Carlo Simulations (Stochastic Forecasting)"):
            st.markdown("""
            Utilizing **Geometric Brownian Motion (GBM)**, the engine extracts historical drift and volatility for top bluechip funds. 
            It then simulates 1,000 unique, randomized market paths spanning 1,260 future trading days (5 years) to generate predictive uncertainty bands at the 5th, 50th, and 95th percentiles.
            """)
        with st.expander("2. Markowitz Efficient Frontier (Modern Portfolio Theory)"):
            st.markdown("""
            The engine simulates 10,000 completely random asset allocations across a diverse 5-fund basket. By mapping Expected Return vs. Expected Risk, it programmatically identifies the **Maximum Sharpe Ratio** portfolio and the **Minimum Volatility** portfolio.
            """)

    with tab4:
        st.subheader("Technology Stack")
        st.markdown("The application is entirely Python-native, guaranteeing cross-platform operability without relying on heavy BI tools.")
        
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("**Data Engineering**")
            st.caption("- Python 3.10+\n- Pandas\n- NumPy\n- SQLite3")
        with c2:
            st.markdown("**Data Science & Math**")
            st.caption("- SciPy\n- Statsmodels\n- Datetime")
        with c3:
            st.markdown("**Visualization & UI**")
            st.caption("- Streamlit\n- Plotly Express\n- Matplotlib\n- Seaborn")
            
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("**Project Authored By:** Karan Veer Singh")
        st.markdown("[View on GitHub](https://github.com/karanveersingh05/MutualFundsAnalytics) | [Connect on LinkedIn](https://www.linkedin.com/in/karanveersingh05/)")


