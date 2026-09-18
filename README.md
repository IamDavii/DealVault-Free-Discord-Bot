# 🤖 DealVault Discord Bot

A lightweight, feature-rich Discord bot built using Python and `discord.py`. It includes standard utility commands such as latency check, help menu, and server information display.

---

## 📋 Prerequisites

Before setting up the bot, ensure you have the following installed on your system:
* **Python 3.8 or higher** (Make sure to check *"Add Python to PATH"* during installation).
* A valid **Discord Bot Token**.

---

## 🚀 Quick Setup Guide

Setting up and running the bot is simple and automated:

### 1. Initial Setup
1. Double-click on **`setup.bat`**.
2. The installer will automatically upgrade `pip` and install the required dependencies (`discord.py` and `python-dotenv`).
3. When prompted, enter your **Discord Bot Token**.
4. The setup will create the `token.env` configuration file automatically.

### 2. Launching the Bot
1. Double-click on **`run-bot.bat`**.
2. If the setup was completed correctly, the console will show `Bot online: <YourBotName>`.
3. Keep the terminal window open to keep the bot online.

> ⚠️ **Note:** If you run `run-bot.bat` without completing `setup.bat` first, the system will prompt you to run `setup.bat` first.

---

## 🛠️ Available Commands

All commands use Discord's modern **Slash Commands** (`/`):

| Command | Description |
| :--- | :--- |
| `/ping` | Displays the current latency and response time of the bot. |
| `/server` | Displays detailed information about the current server (Owner, Member Count, Boosts, Creation Date, etc.). |
| `/help` | Shows the full list of available bot commands. |
| `/userinfo` | Displays detailed profile information about a user (Account creation, Join date, Roles, ID). |