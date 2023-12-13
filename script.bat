@echo off
REM Navigate to the script directory or exit if it fails
cd %~dp0 || exit /b

REM Activate the virtual environment
call venv\Scripts\activate

REM Run your Python script with all arguments passed in
python src/script.py %*

REM Deactivate the virtual environment
call deactivate
