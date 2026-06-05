import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pandas as pd
from pathlib import Path
import os
import datetime

# Setup paths
data_dir = Path('data/processed')
reports_dir = Path('reports')
reports_dir.mkdir(parents=True, exist_ok=True)

def generate_html_report():
    try:
        scorecard = pd.read_csv(data_dir / 'fund_scorecard.csv')
        master = pd.read_csv(data_dir / '01_fund_master_clean.csv')
        # Merge to get the category
        df = pd.merge(scorecard, master[['amfi_code', 'category']], on='amfi_code', how='left')
        # Sort by composite score and take top 5
        top_5 = df.sort_values('scorecard_0_100', ascending=False).head(5)
    except Exception as e:
        print(f"Error reading data: {e}")
        return "<p>Error generating report data.</p>"
        
    date_str = datetime.datetime.now().strftime("%B %d, %Y")
    
    html = f"""
    <html>
      <head>
        <style>
          body {{ font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; color: #333; }}
          .container {{ max-width: 650px; margin: 0 auto; padding: 20px; border: 1px solid #eaeaea; border-radius: 10px; }}
          .header {{ text-align: center; background-color: #1D1D1F; color: white; padding: 20px; border-radius: 8px 8px 0 0; }}
          .content {{ padding: 20px; }}
          h2 {{ color: #1D1D1F; font-size: 1.4rem; border-bottom: 2px solid #E5E5EA; padding-bottom: 10px; }}
          table {{ width: 100%; border-collapse: collapse; margin-top: 20px; font-size: 0.95rem; }}
          th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #E5E5EA; }}
          th {{ background-color: #F5F5F7; font-weight: 600; color: #86868B; text-transform: uppercase; font-size: 0.8rem; letter-spacing: 0.05em; }}
          .footer {{ margin-top: 30px; font-size: 12px; color: #86868B; text-align: center; border-top: 1px solid #eaeaea; padding-top: 15px; }}
          .highlight-score {{ color: #34C759; font-weight: bold; font-size: 1.1rem; }}
        </style>
      </head>
      <body>
        <div class="container">
          <div class="header">
            <h1 style="margin:0; font-size:1.8rem; font-weight:600;">BlueStock Mutual Funds Analytics</h1>
            <p style="margin:5px 0 0 0; color:#A1A1A6;">Weekly Performance Summary</p>
          </div>
          <div class="content">
            <p>Hello Team,</p>
            <p>Here is your automated mutual fund performance update for <strong>{date_str}</strong>.</p>
            <h2>Top 5 Funds by Composite Score</h2>
            <table>
              <tr>
                <th>Scheme Name</th>
                <th>Category</th>
                <th>3Y Return (CAGR)</th>
                <th>Overall Score</th>
              </tr>
    """
    
    for _, row in top_5.iterrows():
        category = row.get('category', 'N/A')
        cagr = round(row.get('cagr_3y', 0) * 100, 2)
        score = round(row.get('scorecard_0_100', 0), 1)
        name = row.get('scheme_name', 'Unknown Scheme')
        
        html += f"""
              <tr>
                <td style="font-weight:500; color:#007AFF;">{name}</td>
                <td>{category}</td>
                <td>{cagr}%</td>
                <td class="highlight-score">{score}/100</td>
              </tr>
        """
        
    html += """
            </table>
            <p style="margin-top: 25px; font-size:0.9rem; color:#555;">
              These scores are generated via the Bluestock factor-weighting model analyzing Sharpe, Alpha, Expense Ratios, and max drawdowns.
              <br><br>
              For more details, please launch the interactive Streamlit dashboard.
            </p>
          </div>
          <div class="footer">
            <p>Automated by Bluestock MF Capstone Pipeline | Made by Karan Veer Singh<br>
            <a href="https://www.linkedin.com/in/karanveersingh05/" style="color:#007AFF;">Connect on LinkedIn</a></p>
          </div>
        </div>
      </body>
    </html>
    """
    return html

def send_email(html_content):
    sender_email = os.environ.get("BLUESTOCK_EMAIL_SENDER", "")
    sender_password = os.environ.get("BLUESTOCK_EMAIL_PASSWORD", "")
    receiver_email = os.environ.get("BLUESTOCK_EMAIL_RECEIVER", "")
    
    # Save a local copy of the HTML for review
    report_path = reports_dir / 'weekly_summary.html'
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"  [HTML] Generated email template saved to: {report_path}")
    
    if not sender_email or not sender_password or not receiver_email:
        print("  [MAIL] Environment variables BLUESTOCK_EMAIL_SENDER/PASSWORD/RECEIVER not found.")
        print("  [MAIL] Skipping live SMTP transmission. The email layout was saved to reports/weekly_summary.html")
        return

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Bluestock MF: Weekly Performance Report"
    msg["From"] = sender_email
    msg["To"] = receiver_email
    
    part = MIMEText(html_content, "html")
    msg.attach(part)
    
    try:
        # Assumes Gmail SMTP
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        print("  [MAIL] Email sent successfully!")
    except Exception as e:
        print(f"  [MAIL] Failed to send email via SMTP: {e}")

if __name__ == "__main__":
    print("Generating Automated Email Report...")
    html_report = generate_html_report()
    send_email(html_report)
    print("Email report generation step completed.")
