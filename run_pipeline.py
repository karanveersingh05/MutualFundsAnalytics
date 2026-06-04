"""
Master Execution Script for Bluestock MF Capstone
Runs the entire ETL, EDA, and Analytics pipeline.
"""
import os
import subprocess

def run_script(script_name):
    print(f"Running {script_name}...")
    result = subprocess.run(['python', script_name], cwd='scripts')
    if result.returncode != 0:
        print(f"Error running {script_name}")
        exit(1)

if __name__ == '__main__':
    scripts = [
        'live_nav_fetch.py',
        'data_ingestion.py',
        'data_cleaning.py',
        'compute_metrics.py',
        'generate_eda.py',
        'generate_advanced_analytics.py',
        'generate_dashboard_mocks.py'
    ]
    for script in scripts:
        run_script(script)
    print("Pipeline executed successfully.")
