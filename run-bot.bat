@echo off
title DealVault Bot - Launcher
:: Sposta la directory di lavoro alla cartella padre (principale)
cd /d "%~dp0.."

echo ===================================
echo       DealVault Bot Launcher
echo ===================================
echo.

if not exist token.env (
    echo [ERROR] 'token.env' file not found!
    echo Please run 'setup.bat' first to configure the bot token and install dependencies.
    echo.
    pause
    exit /b
)

echo Starting the bot...
echo.
python main.py

echo.
echo Bot process stopped.
pause