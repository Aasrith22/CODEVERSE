@echo off
echo ========================================
echo Enhanced Traffic Prediction with CrewAI
echo ========================================
echo.

echo Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

echo Python found!
echo.

echo Installing required dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    echo Please check your internet connection and try again
    pause
    exit /b 1
)

echo.
echo Dependencies installed successfully!
echo.

echo Starting the Enhanced Traffic Prediction System...
echo.
echo The application will be available at: http://localhost:5000
echo Press Ctrl+C to stop the server
echo.

python app.py
