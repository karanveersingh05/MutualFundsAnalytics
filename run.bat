@echo off
title Bluestock MF Analytics Platform
color 0A

echo.
echo ============================================================
echo   BLUESTOCK MUTUAL FUND ANALYTICS PLATFORM
echo   Full Pipeline Runner
echo ============================================================
echo.

:: ── Step 1: Check Python ────────────────────────────────────────────────────
echo [1/4] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo  ERROR: Python is not installed or not on PATH.
    echo  Please install Python 3.10+ from https://www.python.org/downloads/
    echo  Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)
for /f "tokens=*" %%i in ('python --version') do echo  Found: %%i
echo.

:: ── Step 2: Upgrade pip silently ────────────────────────────────────────────
echo [2/4] Upgrading pip...
python -m pip install --upgrade pip --quiet
echo  pip up to date.
echo.

:: ── Step 3: Install all dependencies ────────────────────────────────────────
echo [3/4] Installing dependencies from requirements.txt...
echo  (This may take a few minutes on first run)
echo.
python -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo.
    echo  ERROR: Dependency installation failed.
    echo  Check your internet connection and try again.
    echo.
    pause
    exit /b 1
)
echo.
echo  All dependencies installed successfully.
echo.

:: ── Step 4: Run the pipeline ────────────────────────────────────────────────
echo [4/4] Running analytics pipeline...
echo ============================================================
echo.
python run_pipeline.py
if %errorlevel% neq 0 (
    echo.
    echo ============================================================
    echo  PIPELINE FAILED. Check the error messages above.
    echo ============================================================
    echo.
    pause
    exit /b 1
)

echo.
echo ============================================================
echo  PIPELINE COMPLETE!
echo.
echo  Outputs:
echo    Charts    : reports\charts\
echo    Database  : data\db\bluestock_mf.db
echo    Notebooks : notebooks\
echo    Scorecard : data\processed\fund_scorecard.csv
echo    VaR report: data\processed\var_cvar_report.csv
echo ============================================================
echo.
pause
