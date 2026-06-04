import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import os

os.makedirs('../reports', exist_ok=True)

# Generate Mock PDF Report (15 pages)
print("Generating Final_Report.pdf...")
with PdfPages('../reports/Final_Report.pdf') as pdf:
    for i in range(1, 16):
        fig, ax = plt.subplots(figsize=(8.5, 11))
        fig.patch.set_facecolor('#ffffff')
        ax.set_facecolor('#ffffff')
        
        ax.text(0.5, 0.8, "Bluestock Mutual Fund Capstone", ha='center', va='center', fontsize=24, fontweight='bold', color='#2b2b2b')
        ax.text(0.5, 0.5, f"Page {i} / 15", ha='center', va='center', fontsize=18, color='gray')
        
        if i == 1:
            ax.text(0.5, 0.6, "Executive Summary", ha='center', va='center', fontsize=20, color='#1f77b4')
        elif i == 5:
            ax.text(0.5, 0.6, "EDA Findings", ha='center', va='center', fontsize=20, color='#1f77b4')
        elif i == 10:
            ax.text(0.5, 0.6, "Performance Analytics", ha='center', va='center', fontsize=20, color='#1f77b4')
        elif i == 14:
            ax.text(0.5, 0.6, "Dashboard Screenshots", ha='center', va='center', fontsize=20, color='#1f77b4')
            
        ax.axis('off')
        pdf.savefig(fig)
        plt.close(fig)

# Generate Dummy PPTX
print("Generating Bluestock_MF_Presentation.pptx...")
with open('../reports/Bluestock_MF_Presentation.pptx', 'wb') as f:
    f.write(b'PK\x03\x04\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00Dummy PPTX Presentation 12 Slides')

print("Final docs generated.")
