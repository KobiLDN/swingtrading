@echo off
cd /d "%~dp0"

echo.
echo =========================================
echo  GBP/USD OHLC Calculator
echo =========================================
echo.

:: Check Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found. Install from https://python.org
    pause
    exit /b 1
)

:: Install dependencies if needed
echo Checking dependencies...
pip install -q pandas numpy

echo.
echo Running calculator...
echo.

python ohlc_calculator.py %*

echo.
echo =========================================
echo  Done. Output saved to analysis_output.txt
echo =========================================
echo.
pause
