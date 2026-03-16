@echo off
REM MNIST ANN Setup Script for Windows
REM This script sets up a virtual environment and installs all dependencies

setlocal enabledelayedexpansion

set "PROJECT_DIR=%~dp0"
set "VENV_DIR=%PROJECT_DIR%venv"

echo.
echo ======================================================
echo   MNIST ANN Project Setup
echo ======================================================
echo.
echo Project directory: %PROJECT_DIR%
echo.

REM Check if virtual environment already exists
if exist "%VENV_DIR%" (
    echo [OK] Virtual environment already exists
) else (
    echo [*] Creating virtual environment...
    python -m venv "%VENV_DIR%"
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment
        exit /b 1
    )
    echo [OK] Virtual environment created successfully
)

echo.
echo [*] Activating virtual environment...
call "%VENV_DIR%\Scripts\activate.bat"

echo.
echo [*] Installing dependencies...
pip install --upgrade pip setuptools wheel -q
pip install -r "%PROJECT_DIR%requirements.txt" -q

if errorlevel 1 (
    echo [ERROR] Failed to install dependencies
    exit /b 1
)

echo [OK] Dependencies installed successfully

echo.
echo ======================================================
echo   Setup Complete!
echo ======================================================
echo.
echo Next steps:
echo   1. Activate: %VENV_DIR%\Scripts\activate.bat
echo   2. Start Jupyter: jupyter notebook
echo   3. Open: mnist_ann.ipynb
echo.
echo Verify installation:
echo   python -c "import numpy, pandas, matplotlib; print('[OK] All packages installed')"
echo.
pause
