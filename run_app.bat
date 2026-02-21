@echo off
REM Check if virtual environment exists
if not exist "env_travel\Scripts\activate.bat" (
    echo.
    echo [ERROR] Virtual environment not found!
    echo Please follow the setup instructions in SETUP.md first.
    echo.
    pause
    exit /b
)

REM Run the Streamlit app
echo Starting Travel Planner AI...
.\env_travel\Scripts\python.exe -m streamlit run TravelCrewApp.py
pause
