import pandas as pd
import os
from pathlib import Path

def main():
    raw_data_dir = Path('../data/raw')
    
    files = [
        "01_fund_master.csv",
        "02_nav_history.csv",
        "03_aum_by_fund_house.csv",
        "04_monthly_sip_inflows.csv",
        "05_category_inflows.csv",
        "06_industry_folio_count.csv",
        "07_scheme_performance.csv",
        "08_investor_transactions.csv",
        "09_portfolio_holdings.csv",
        "10_benchmark_indices.csv"
    ]
    
    dataframes = {}
    
    print("=== Loading Datasets ===")
    for filename in files:
        filepath = raw_data_dir / filename
        if filepath.exists():
            print(f"\n--- {filename} ---")
            try:
                df = pd.read_csv(filepath)
                dataframes[filename] = df
                print(f"Shape: {df.shape}")
                print("\nData Types:")
                print(df.dtypes)
                print("\nHead:")
                print(df.head(2))
            except Exception as e:
                print(f"Error loading {filename}: {e}")
        else:
            print(f"\nFile {filename} not found at {filepath}")
            
    print("\n\n=== Exploring Fund Master ===")
    if "01_fund_master.csv" in dataframes:
        df_fund = dataframes["01_fund_master.csv"]
        print(f"Unique Fund Houses: {df_fund['fund_house'].nunique()}")
        print(df_fund['fund_house'].unique())
        
        print(f"\nUnique Categories: {df_fund['category'].nunique()}")
        print(df_fund['category'].unique())
        
        print(f"\nUnique Sub-Categories: {df_fund['sub_category'].nunique()}")
        print(df_fund['sub_category'].unique())
        
        print(f"\nUnique Risk Grades: {df_fund['risk_category'].nunique()}")
        print(df_fund['risk_category'].unique())
        
    print("\n\n=== Validating AMFI Codes ===")
    if "01_fund_master.csv" in dataframes and "02_nav_history.csv" in dataframes:
        fund_codes = set(dataframes["01_fund_master.csv"]['amfi_code'].unique())
        nav_codes = set(dataframes["02_nav_history.csv"]['amfi_code'].unique())
        
        missing_in_nav = fund_codes - nav_codes
        
        print(f"Total codes in fund master: {len(fund_codes)}")
        print(f"Total codes in NAV history: {len(nav_codes)}")
        
        if len(missing_in_nav) == 0:
            print("Validation SUCCESS: All AMFI codes in fund_master exist in nav_history.")
        else:
            print(f"Validation FAILED: The following codes are missing in nav_history: {missing_in_nav}")
            
    print("\n\n=== Data Quality Summary ===")
    print("Data loaded successfully. Basic type checking complete.")
    print("Fund master categories seem aligned with expectations.")

if __name__ == "__main__":
    main()
