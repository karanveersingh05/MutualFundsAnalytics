@echo off
title Setup ETL Scheduled Task
color 0A

echo ============================================================
echo   BLUESTOCK MUTUAL FUND ANALYTICS PLATFORM
echo   ETL Windows Task Scheduler Setup
echo ============================================================
echo.
echo This script will create a Windows Scheduled Task to run the 
echo run_pipeline.py script every weekday (Mon-Fri) at 8:00 PM.
echo.
pause

set TASK_NAME=Bluestock_MF_ETL_AutoFetch
set SCRIPT_PATH=%~dp0run_pipeline.py
set PYTHON_EXE=python

echo.
echo Creating Scheduled Task...
schtasks /create /tn "%TASK_NAME%" /tr "%PYTHON_EXE% \"%SCRIPT_PATH%\"" /sc weekly /d MON,TUE,WED,THU,FRI /st 20:00 /f

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Failed to create scheduled task. Try running as Administrator.
) else (
    echo.
    echo Task created successfully!
    echo The ETL pipeline will now run automatically at 8:00 PM every weekday.
    echo You can manage this task in Windows "Task Scheduler".
)
echo.
pause
