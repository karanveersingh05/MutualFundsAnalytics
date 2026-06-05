"""
schedule_etl.py
Schedules the ETL pipeline to run every weekday at 8:00 PM.
Usage: python schedule_etl.py (Keep terminal open)
"""
import time
import subprocess
import sys
from pathlib import Path

try:
    import schedule
except ImportError:
    print("Error: 'schedule' library not found. Install it using: pip install schedule")
    sys.exit(1)

# We run live_nav_fetch.py or the full pipeline. Let's run the pipeline.
PIPELINE_SCRIPT = Path(__file__).parent.parent / "run_pipeline.py"

def run_etl():
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Running Scheduled ETL...")
    result = subprocess.run([sys.executable, str(PIPELINE_SCRIPT)])
    if result.returncode == 0:
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] ETL execution completed successfully.")
    else:
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] ETL execution failed with exit code {result.returncode}.")

# Schedule for every weekday at 8 PM (20:00)
schedule.every().monday.at("20:00").do(run_etl)
schedule.every().tuesday.at("20:00").do(run_etl)
schedule.every().wednesday.at("20:00").do(run_etl)
schedule.every().thursday.at("20:00").do(run_etl)
schedule.every().friday.at("20:00").do(run_etl)

if __name__ == "__main__":
    print("============================================================")
    print("              Bluestock MF ETL Scheduler                    ")
    print("============================================================")
    print(f"Target script: {PIPELINE_SCRIPT}")
    print("Scheduled to run Monday to Friday at 20:00 (8:00 PM).")
    print("Keep this window open to process the schedule...")
    print("============================================================")
    
    while True:
        schedule.run_pending()
        time.sleep(60) # check every minute
