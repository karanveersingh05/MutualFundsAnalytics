import pandas as pd
import argparse
import warnings
warnings.filterwarnings('ignore')

def recommend(risk_appetite):
    processed_dir = 'data/processed'
    df_fund = pd.read_csv(f'{processed_dir}/01_fund_master_clean.csv')
    df_score = pd.read_csv(f'{processed_dir}/fund_scorecard.csv')
    
    df = df_score.merge(df_fund[['amfi_code', 'risk_category']], on='amfi_code')
    
    # Map input to risk_category from DB
    mapping = {
        'Low': ['Low', 'Low to Moderate'],
        'Moderate': ['Moderate', 'Moderately High'],
        'High': ['High', 'Very High']
    }
    
    allowed_risks = mapping.get(risk_appetite, ['Moderate'])
    
    df_filtered = df[df['risk_category'].isin(allowed_risks)]
    if df_filtered.empty:
        # Fallback if mapping missed
        df_filtered = df[df['risk_category'].str.contains(risk_appetite, case=False, na=False)]
        if df_filtered.empty:
            df_filtered = df
            
    top_3 = df_filtered.sort_values('sharpe', ascending=False).head(3)
    
    print(f"\\n--- Top 3 Funds for {risk_appetite} Risk Appetite ---")
    for idx, row in top_3.iterrows():
        print(f"{row['scheme_name']} | Risk: {row['risk_category']} | Sharpe: {row['sharpe']:.2f}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Simple Fund Recommender')
    parser.add_argument('--risk', type=str, choices=['Low', 'Moderate', 'High'], default='Moderate', help='Risk Appetite')
    args = parser.parse_args()
    recommend(args.risk)
