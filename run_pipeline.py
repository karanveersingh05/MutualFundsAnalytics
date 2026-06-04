"""
run_pipeline.py
Master execution script — runs the full ETL + analytics pipeline.
Usage: python run_pipeline.py
"""
import subprocess
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).parent / 'scripts'

PIPELINE = [
    'live_nav_fetch.py',
    'data_ingestion.py',
    'data_cleaning.py',
    'run_eda.py',
    'compute_metrics.py',
    'generate_advanced_analytics.py',
    'generate_dashboard_mocks.py',
    'generate_final_docs.py',
]

def run_script(name: str) -> None:
    path = SCRIPTS_DIR / name
    if not path.exists():
        print(f"  SKIP — {name} not found")
        return
    print(f"\n{'='*60}\nRunning {name}...\n{'='*60}")
    result = subprocess.run(
        [sys.executable, str(path)],
        cwd=str(SCRIPTS_DIR)          # each script resolves paths relative to scripts/
    )
    if result.returncode != 0:
        print(f"\nERROR in {name} (exit {result.returncode}) — pipeline halted.")
        sys.exit(result.returncode)
    print(f"  {name} DONE")


if __name__ == '__main__':
    print("Bluestock MF Analytics Pipeline — Start")
    for script in PIPELINE:
        run_script(script)
    print("\nPipeline completed successfully.")
