@echo off
echo ========================================
echo Zenith Study Buddy - SQLite Setup
echo (No database installation needed!)
echo ========================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.11+ from https://www.python.org/
    pause
    exit /b 1
)

REM Check Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js is not installed or not in PATH
    echo Please install Node.js 18+ from https://nodejs.org/
    pause
    exit /b 1
)

echo ========================================
echo Setting up Backend (with SQLite)
echo ========================================
cd backend

REM Create virtual environment
if not exist "venv" (
    echo Creating Python virtual environment...
    python -m venv venv
)

REM Activate and install
echo Installing backend dependencies...
call venv\Scripts\activate.bat
pip install -r requirements.txt

REM Setup environment file for SQLite
if not exist ".env" (
    echo Creating backend .env file with SQLite...
    echo DATABASE_URL=sqlite:///./zenith_study_buddy.db > .env
    echo SECRET_KEY=development-secret-key-change-in-production >> .env
    echo OMNIDIM_API_KEY=your-omnidim-api-key >> .env
    echo.
    echo IMPORTANT: Edit backend\.env and add your Omnidim API key!
    echo.
)

REM Initialize SQLite database
echo.
echo Creating SQLite database...
python scripts\init_sqlite.py

REM Seed database
python scripts\seed_data.py

echo.
echo Backend setup complete with SQLite!
echo.

REM Setup Frontend (same as before)
echo ========================================
echo Setting up Frontend
echo ========================================
cd ..\frontend

echo Installing frontend dependencies...
call npm install

if not exist ".env.local" (
    echo Creating frontend .env.local file...
    echo NEXT_PUBLIC_API_URL=http://localhost:8000/api > .env.local
    echo NEXT_PUBLIC_WS_URL=ws://localhost:8000 >> .env.local
    echo NEXT_PUBLIC_OMNIDIM_API_KEY=your-omnidim-api-key >> .env.local
)

cd ..
echo ========================================
echo Setup Complete! No database server needed!
echo ========================================
echo.
echo The SQLite database file is at:
echo   backend\zenith_study_buddy.db
echo.
echo Next steps:
echo 1. Edit backend\.env and add your Omnidim API key
echo 2. Edit frontend\.env.local and add your Omnidim API key
echo 3. Run start-sqlite.bat to start the application
echo.
pause