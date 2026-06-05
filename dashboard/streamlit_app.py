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

# --- Paths ---
BASE_DIR = Path(__file__).parent.parent
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
    "Send Report"
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
        st.image(str(chart_path), caption="Monte Carlo NAV Bands (5th / 50th / 95th percentile)", use_column_width=True)
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
        st.image(str(chart_path), caption="Efficient Frontier: Each dot = one simulated portfolio", use_column_width=True)
    else:
        st.warning("Chart not found. Please run the pipeline first via run.bat.")

# =============================================================================
# Page 7: Send Report (Task 13 - integrated in the web app)
# =============================================================================
elif page == "Send Report":
    st.title("Weekly Performance Report")
    st.markdown("Generate and send an automated HTML performance email directly from the dashboard.")
    st.markdown("<br>", unsafe_allow_html=True)

    # --- HTML preview ---
    def generate_html_report(data):
        """Build the HTML email body from current scorecard data."""
        try:
            scorecard = data['scorecard']
            master = data['fund_master']
            df = pd.merge(scorecard, master[['amfi_code', 'category']], on='amfi_code', how='left')
            top_5 = df.sort_values('scorecard_0_100', ascending=False).head(5)
        except Exception as e:
            return f"<p>Error generating report: {e}</p>"

        date_str = datetime.datetime.now().strftime("%B %d, %Y")

        rows_html = ""
        for _, row in top_5.iterrows():
            cagr = round(row.get('cagr_3y', 0) * 100, 2)
            score = round(row.get('scorecard_0_100', 0), 1)
            rows_html += f"""
            <tr>
              <td style="font-weight:500; color:#007AFF;">{row.get('scheme_name','')}</td>
              <td>{row.get('category','N/A')}</td>
              <td>{cagr}%</td>
              <td style="color:#34C759; font-weight:bold;">{score}/100</td>
            </tr>"""

        return f"""<html><head>
        <style>
          body{{font-family:'Helvetica Neue',Arial,sans-serif;color:#333;background:#F5F5F7;}}
          .wrap{{max-width:650px;margin:30px auto;background:#fff;border-radius:12px;overflow:hidden;border:1px solid #eaeaea;}}
          .hd{{background:#1D1D1F;color:#fff;padding:25px;text-align:center;}}
          .body{{padding:25px;}}
          table{{width:100%;border-collapse:collapse;margin-top:15px;}}
          th,td{{padding:12px;text-align:left;border-bottom:1px solid #E5E5EA;font-size:0.9rem;}}
          th{{background:#F5F5F7;font-weight:600;color:#86868B;text-transform:uppercase;font-size:0.78rem;letter-spacing:.05em;}}
          .ft{{padding:15px;text-align:center;font-size:11px;color:#86868B;border-top:1px solid #eaeaea;}}
        </style></head><body>
        <div class="wrap">
          <div class="hd"><h2 style="margin:0;font-size:1.5rem;">BlueStock Mutual Funds Analytics</h2>
          <p style="margin:5px 0 0;color:#A1A1A6;font-size:.9rem;">Weekly Performance Summary — {date_str}</p></div>
          <div class="body">
            <p>Hello,</p>
            <p>Here are the <strong>Top 5 Funds</strong> by composite score as of {date_str}.</p>
            <table>
              <tr><th>Scheme Name</th><th>Category</th><th>3Y CAGR</th><th>Score</th></tr>
              {rows_html}
            </table>
            <p style="margin-top:20px;font-size:.85rem;color:#555;">
              Scores reflect Sharpe, Alpha, Expense Ratio, and Max Drawdown factors.<br>
              View the full interactive dashboard via Streamlit.
            </p>
          </div>
          <div class="ft">Automated by BlueStock MF Pipeline |
            Made by <a href="https://www.linkedin.com/in/karanveersingh05/" style="color:#007AFF;">Karan Veer Singh</a>
          </div>
        </div></body></html>"""

    html_content = generate_html_report(data)

    # Preview
    with st.expander("Preview Email HTML", expanded=True):
        st.components.v1.html(html_content, height=520, scrolling=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("Send via Gmail")
    st.info("Uses Gmail SMTP with an App Password. Generate one at myaccount.google.com > Security > App Passwords.")

    with st.form("email_form"):
        sender_email = st.text_input("Your Gmail Address", placeholder="you@gmail.com")
        sender_password = st.text_input("Gmail App Password", type="password", placeholder="16-char app password")
        receiver_email = st.text_input("Recipient Email", placeholder="recipient@example.com")
        submitted = st.form_submit_button("Send Report")

    if submitted:
        if not sender_email or not sender_password or not receiver_email:
            st.error("All three fields are required.")
        else:
            try:
                msg = MIMEMultipart("alternative")
                msg["Subject"] = f"BlueStock MF: Weekly Report — {datetime.datetime.now().strftime('%d %b %Y')}"
                msg["From"] = sender_email
                msg["To"] = receiver_email
                msg.attach(MIMEText(html_content, "html"))

                with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                    server.login(sender_email, sender_password)
                    server.sendmail(sender_email, receiver_email, msg.as_string())

                # Also save local HTML copy
                report_path = BASE_DIR / 'reports' / 'weekly_summary.html'
                report_path.write_text(html_content, encoding='utf-8')

                st.success(f"Report sent successfully to {receiver_email}!")
            except smtplib.SMTPAuthenticationError:
                st.error("Authentication failed. Check your Gmail and App Password.")
            except Exception as e:
                st.error(f"Failed to send: {e}")
