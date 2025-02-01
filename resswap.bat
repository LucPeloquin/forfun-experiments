@echo off
:: Check for elevated permissions
net session >nul 2>&1
if %errorLevel% NEQ 0 (
    echo Requesting administrative privileges...
    powershell -Command "Start-Process cmd -ArgumentList '/c, %~dp0%~nx0' -Verb runAs"
    exit /b
)

:: Run the PowerShell script in the 'scripts' subfolder
powershell -ExecutionPolicy Bypass -File "%~dp0scripts\resolutionswap.ps1"
