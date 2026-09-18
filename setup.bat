@echo off
title DealVault Bot - Setup
:: Sposta la directory di lavoro alla cartella padre (principale)
cd /d "%~dp0.."

echo ===================================
echo    DealVault Bot Setup Installer
echo ===================================
echo.

echo Installing required Python libraries...
python -m pip install --upgrade pip
python -m pip install -U discord.py python-dotenv

echo.
echo ===================================
echo    Discord Bot Token Configuration
echo ===================================
echo.

:ask_token
set /p BOT_TOKEN="Please enter your Discord Bot Token: "

if "%BOT_TOKEN%"=="" (
    echo [ERROR] Token cannot be empty. Please try again.
    goto ask_token
)

echo Writing token to token.env...
> token.env echo DISCORD_TOKEN=%BOT_TOKEN%

echo.
echo ===================================
echo Setup completed successfully!
echo You can now run 'start.bat' to launch the bot.
echo ===================================
echo.
pause