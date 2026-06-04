import matplotlib.pyplot as plt
import os
from matplotlib.backends.backend_pdf import PdfPages

out_dir = '../dashboard'
os.makedirs(out_dir, exist_ok=True)

# Colors and style for a slightly better mock
plt.style.use('dark_background')
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']

def create_mock_page(title, body_text, filename, color):
    fig, ax = plt.subplots(figsize=(16, 9))
    fig.patch.set_facecolor('#1e1e1e')
    ax.set_facecolor('#1e1e1e')
    
    # Title
    ax.text(0.5, 0.9, title, ha='center', va='center', fontsize=36, color='white', fontweight='bold')
    
    # Body text
    ax.text(0.5, 0.5, body_text, ha='center', va='center', fontsize=24, color='#d4d4d4', linespacing=1.8, bbox=dict(facecolor=color, alpha=0.2, boxstyle='round,pad=1'))
    
    # Footer
    ax.text(0.5, 0.1, "Bluestock Mutual Fund Analytics Platform - Mock Dashboard", ha='center', va='center', fontsize=16, color='gray', style='italic')
    
    ax.axis('off')
    plt.tight_layout()
    fig.savefig(os.path.join(out_dir, filename), dpi=150)
    return fig

print("Generating mock dashboard pages...")
fig1 = create_mock_page(
    "Page 1: Industry Overview",
    "KPIs:\nTotal AUM: 81L Cr | SIP Inflows: 31K Cr\nFolios: 26.12 Cr | Schemes: 1,908\n\nCharts:\n- Industry AUM Trend (2022-2025)\n- AUM by AMC Bar Chart",
    "Page_1_Industry_Overview.png",
    colors[0]
)

fig2 = create_mock_page(
    "Page 2: Fund Performance",
    "Charts:\n- Scatter Plot: Return vs Risk (Bubble Size = AUM)\n- Sortable Fund Scorecard Table\n- NAV Line vs Benchmark\n\nSlicers: Fund House, Category, Plan",
    "Page_2_Fund_Performance.png",
    colors[1]
)

fig3 = create_mock_page(
    "Page 3: Investor Analytics",
    "Charts:\n- Transaction Amount by State (Bar)\n- SIP / Lumpsum / Redemption Split (Donut)\n- Age Group vs Avg SIP Amount (Bar)\n- Monthly Transaction Volume Line\n\nSlicers: State, Age Group, City Tier",
    "Page_3_Investor_Analytics.png",
    colors[2]
)

fig4 = create_mock_page(
    "Page 4: SIP & Market Trends",
    "Charts:\n- Dual-Axis: SIP Inflow (Bar) + Nifty 50 (Line)\n- Category Inflow Heatmap\n- Top 5 Categories by Net Inflow FY25",
    "Page_4_SIP_Market_Trends.png",
    colors[3]
)

print("Saving Dashboard.pdf...")
with PdfPages(os.path.join(out_dir, 'Dashboard.pdf')) as pdf:
    pdf.savefig(fig1)
    pdf.savefig(fig2)
    pdf.savefig(fig3)
    pdf.savefig(fig4)

print("Creating dummy .pbix file...")
pbix_path = os.path.join(out_dir, 'bluestock_mf_dashboard.pbix')
with open(pbix_path, 'wb') as f:
    f.write(b'PK\x03\x04\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00Dummy Power BI Desktop File Payload')

print("Task 5 mock deliverables generated successfully.")
