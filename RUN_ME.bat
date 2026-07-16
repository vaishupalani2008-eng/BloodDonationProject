@echo off
ECHO.
ECHO ========================================
ECHO Blood Donation Camp Management System
ECHO ========================================
ECHO.
ECHO Starting the application...
ECHO.
ECHO Open your browser and go to:
ECHO http://localhost:5000
ECHO.
ECHO ========================================
ECHO.

IF EXIST "%~dp0.venv\Scripts\activate.bat" (
    CALL "%~dp0.venv\Scripts\activate.bat"
) ELSE (
    ECHO Warning: Local virtual environment not found. Running system Python.
)

python app.py

PAUSE
