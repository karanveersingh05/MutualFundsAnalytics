"""
streamlit_app.py
Bluestock Mutual Fund Analytics Platform - Streamlit Web App
"""
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# --- Page Config ---
st.set_page_config(page_title="Bluestock MF Analytics", layout="wide", initial_sidebar_state="expanded")

# --- Custom Apple-like CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .stApp {
        background-color: #F5F5F7; /* Apple light gray background */
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
    
    /* Metric Cards */
    div[data-testid="stMetricValue"] {
        font-size: 2.2rem !important;
        font-weight: 600;
        color: #1D1D1F;
    }
    
    div[data-testid="stMetricLabel"] {
        font-size: 0.95rem !important;
        font-weight: 500;
        color: #86868B;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    div[data-testid="stMetricDelta"] {
        font-weight: 500;
    }

    /* Container padding adjustments */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1400px; /* Prevent over-stretching on huge monitors */
    }
    
    /* Clean DataFrame tables */
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

# --- Data Loading ---
@st.cache_data
def load_data():
    base_dir = Path(__file__).parent.parent / 'data' / 'processed'
    data = {}
    try:
        data['fund_master'] = pd.read_csv(base_dir / '01_fund_master_clean.csv')
        data['aum'] = pd.read_csv(base_dir / '03_aum_by_fund_house_clean.csv')
        data['sip'] = pd.read_csv(base_dir / '04_monthly_sip_inflows_clean.csv')
        data['category_inflows'] = pd.read_csv(base_dir / '05_category_inflows_clean.csv')
        data['scorecard'] = pd.read_csv(base_dir / 'fund_scorecard.csv')
        data['transactions'] = pd.read_csv(base_dir / '08_investor_transactions_clean.csv')
    except Exception as e:
        st.error(f"Error loading data: {e}")
    return data

data = load_data()

# --- Sidebar Navigation ---
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/e/eb/Apple_logo_black.svg", width=40) # Aesthetic placeholder
st.sidebar.markdown("""
<div style='margin-bottom: 20px;'>
    <h2 style='margin-bottom: 8px; line-height: 1.2;'>BlueStock<br>Mutual Funds<br>Analytics</h2>
    <span style='font-size: 0.85rem; color: #86868B;'>Made By <a href='https://www.linkedin.com/in/karanveersingh05/' target='_blank' style='color: #007AFF; text-decoration: none; font-weight: 500;'>Karan Veer Singh</a></span>
</div>
""", unsafe_allow_html=True)
st.sidebar.markdown("---")
page = st.sidebar.radio("Navigation", 
    ["Industry Overview", "Fund Performance", "Investor Analytics", "SIP Trends"]
)

st.sidebar.markdown("---")
st.sidebar.caption("v1.3 | Built for Capstone")

if not data:
    st.stop()

# --- Page 1: Industry Overview ---
if page == "Industry Overview":
    st.title("Industry Overview")
    st.markdown("Macro-level view of the Indian Mutual Fund Industry.")
    st.markdown("<br>", unsafe_allow_html=True)
    
    # KPI Row
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
            # Group by fund_house and take the max AUM overall
            latest_aum = data['aum'].groupby('fund_house')['aum_crore'].max().reset_index().sort_values('aum_crore', ascending=False).head(10)
            fig = px.bar(latest_aum, x='fund_house', y='aum_crore', 
                         color='fund_house',
                         color_discrete_sequence=px.colors.qualitative.Pastel)
            fig.update_layout(**plotly_layout, showlegend=False, xaxis_title="", yaxis_title="AUM (₹ Cr)")
            st.plotly_chart(fig, use_container_width=True)
            
    with col_b:
        st.subheader("Category Net Inflows (FY25)")
        if 'category_inflows' in data:
            cat_sum = data['category_inflows'].groupby('category')['net_inflow_crore'].sum().reset_index()
            fig = px.pie(cat_sum, names='category', values='net_inflow_crore', hole=0.6,
                         color_discrete_sequence=px.colors.qualitative.Set2)
            fig.update_layout(**plotly_layout, showlegend=False)
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)

# --- Page 2: Fund Performance ---
elif page == "Fund Performance":
    st.title("Fund Performance & Risk")
    st.markdown("Compare risk-adjusted returns across the Bluestock universe.")
    st.markdown("<br>", unsafe_allow_html=True)
    
    if 'scorecard' in data and 'fund_master' in data:
        # Merge scorecard with master to get fund_house and category
        df_score = pd.merge(data['scorecard'], data['fund_master'][['amfi_code', 'fund_house', 'category']], on='amfi_code', how='left')
        
        # Filters
        col1, col2 = st.columns(2)
        with col1:
            amc_list = ["All"] + list(df_score['fund_house'].dropna().unique())
            amc_filter = st.selectbox("Select AMC", amc_list)
        with col2:
            cat_list = ["All"] + list(df_score['category'].dropna().unique())
            cat_filter = st.selectbox("Select Category", cat_list)
            
        filtered_df = df_score.copy()
        if amc_filter != "All":
            filtered_df = filtered_df[filtered_df['fund_house'] == amc_filter]
        if cat_filter != "All":
            filtered_df = filtered_df[filtered_df['category'] == cat_filter]
            
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("Risk vs Return (Alpha vs CAGR)")
        # Plotting cagr_3y vs alpha. Size by scorecard_0_100
        fig = px.scatter(filtered_df, x='cagr_3y', y='alpha', 
                         size='scorecard_0_100', color='category', hover_name='scheme_name',
                         labels={'cagr_3y': 'Return (3 Yr CAGR)', 'alpha': 'Alpha (Excess Return)'},
                         color_discrete_sequence=px.colors.qualitative.Bold)
        fig.update_layout(**plotly_layout)
        # Add subtle grid lines
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#E5E5EA')
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#E5E5EA')
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("Fund Scorecard Ranking")
        
        # Clean dataframe for display
        display_df = filtered_df[['scheme_name', 'fund_house', 'category', 'scorecard_0_100', 'cagr_3y', 'sharpe', 'alpha']].copy()
        display_df.columns = ['Scheme Name', 'AMC', 'Category', 'Score (0-100)', '3Y CAGR', 'Sharpe', 'Alpha']
        display_df = display_df.sort_values('Score (0-100)', ascending=False).reset_index(drop=True)
        
        st.dataframe(display_df, use_container_width=True)

# --- Page 3: Investor Analytics ---
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
            # Apple-like colors
            fig = px.pie(tx_type, names='Type', values='Count', hole=0.5, color_discrete_sequence=['#34C759', '#007AFF', '#FF3B30'])
            fig.update_layout(**plotly_layout)
            st.plotly_chart(fig, use_container_width=True)
            
        with col2:
            st.subheader("City Tier Distribution")
            tier = tx['city_tier'].value_counts().reset_index()
            tier.columns = ['Tier', 'Count']
            fig = px.bar(tier, x='Tier', y='Count', color='Tier', color_discrete_sequence=['#5856D6', '#FF9500'])
            fig.update_layout(**plotly_layout, showlegend=False, xaxis_title="")
            st.plotly_chart(fig, use_container_width=True)
            
        st.markdown("<br><hr style='border:1px solid #E5E5EA'><br>", unsafe_allow_html=True)
        
        st.subheader("Transactions by State")
        state_sum = tx.groupby('state')['amount_inr'].sum().reset_index().sort_values('amount_inr', ascending=False)
        fig = px.bar(state_sum, x='amount_inr', y='state', orientation='h', color='amount_inr', color_continuous_scale='Blues')
        fig.update_layout(**plotly_layout, yaxis={'categoryorder':'total ascending'}, yaxis_title="", xaxis_title="Total Amount (₹)")
        st.plotly_chart(fig, use_container_width=True)

# --- Page 4: SIP & Market Trends ---
elif page == "SIP Trends":
    st.title("SIP & Market Trends")
    st.markdown("Analysing the phenomenal growth of systematic investing in India.")
    st.markdown("<br>", unsafe_allow_html=True)
    
    if 'sip' in data:
        sip = data['sip'].copy()
        
        st.subheader("Monthly SIP Inflows Growth")
        fig = px.area(sip, x='month', y='sip_inflow_crore', 
                      labels={'month': 'Month', 'sip_inflow_crore': 'Inflow (₹ Cr)'},
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
