@echo off
setlocal
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
  echo Creating the Health360 Python environment...
  py -m venv .venv 2>nul
  if errorlevel 1 python -m venv .venv
  if errorlevel 1 goto :python_error
)

call ".venv\Scripts\activate.bat"
".venv\Scripts\python.exe" -c "import flask" >nul 2>&1
if errorlevel 1 (
  echo Installing Flask. This first setup needs an internet connection...
  ".venv\Scripts\python.exe" -m pip install -r requirements.txt
  if errorlevel 1 goto :install_error
)

echo.
echo Health360 is starting.
echo Open http://127.0.0.1:5000 in your browser.
echo Keep this window open while using the app. Press Ctrl+C to stop it.
echo.
".venv\Scripts\python.exe" app.py
goto :end

:python_error
echo Python was not found. Install Python 3.10 or newer, then run this file again.
pause
exit /b 1

:install_error
echo Flask could not be installed. Check your internet connection and try again.
pause
exit /b 1

:end
pause
