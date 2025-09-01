#!/bin/bash

echo "========================================"
echo "Enhanced Traffic Prediction with CrewAI"
echo "========================================"
echo

echo "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo "ERROR: Python is not installed or not in PATH"
        echo "Please install Python 3.8 or higher"
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

echo "Python found!"
echo

echo "Installing required dependencies..."
if ! pip install -r requirements.txt; then
    echo "ERROR: Failed to install dependencies"
    echo "Please check your internet connection and try again"
    exit 1
fi

echo
echo "Dependencies installed successfully!"
echo

echo "Starting the Enhanced Traffic Prediction System..."
echo
echo "The application will be available at: http://localhost:5000"
echo "Press Ctrl+C to stop the server"
echo

$PYTHON_CMD app.py
