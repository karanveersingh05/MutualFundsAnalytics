import pandas as pd
import requests
import json
import os
from pathlib import Path

# Paths
raw_data_dir = Path('../data/raw')
raw_data_dir.mkdir(parents=True, exist_ok=True)

def fetch_and_save_nav(scheme_code, name=""):
    url = f"https://api.mfapi.in/mf/{scheme_code}"
    print(f"Fetching data for {scheme_code} ({name})...")
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        
        # Check if data exists
        if "data" in data and len(data["data"]) > 0:
            df = pd.DataFrame(data["data"])
            
            # Add scheme code and metadata
            df['scheme_code'] = scheme_code
            if "meta" in data and "scheme_name" in data["meta"]:
                df['scheme_name'] = data["meta"]["scheme_name"]
                
            csv_path = raw_data_dir / f"{scheme_code}_live_nav.csv"
            df.to_csv(csv_path, index=False)
            print(f"Successfully saved {scheme_code} NAV to {csv_path}")
        else:
            print(f"No NAV data found for {scheme_code}")
    else:
        print(f"Failed to fetch data for {scheme_code}, status code: {response.status_code}")

def main():
    # Fetch HDFC Top 100 Direct
    fetch_and_save_nav("125497", "HDFC Top 100 Direct")
    
    # Fetch 5 key schemes
    schemes = [
        ("119551", "SBI Bluechip"),
        ("120503", "ICICI Bluechip"),
        ("118632", "Nippon Large Cap"),
        ("119092", "Axis Bluechip"),
        ("120841", "Kotak Bluechip")
    ]
    
    for code, name in schemes:
        fetch_and_save_nav(code, name)
        
if __name__ == "__main__":
    main()
