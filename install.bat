@echo off
chcp 65001 >nul
setlocal

set TASK_NAME=SetTime
set SCRIPT_PATH=C:\TimeFix\set_time.exe

if not exist "%SCRIPT_PATH%" (
    echo Time setter not found!
    pause
    exit /b 1
)

schtasks /query /tn "%TASK_NAME%" >nul 2>&1
if %ERRORLEVEL%==0 (
    echo Deleting previous task
    schtasks /delete /tn "%TASK_NAME%" /f >nul
)

schtasks /create ^
    /tn "%TASK_NAME%" ^
    /tr "%SCRIPT_PATH%" ^
    /sc onlogon ^
    /rl highest ^
    /f

if %ERRORLEVEL% NEQ 0 (
    echo eRROR
    pause
    exit /b 1
)

echo.
echo Task created!
pause
endlocal