# Discord Economy Bot

## Overview
A Discord bot that implements a simple banking/economy system. Users can manage virtual wallets and bank accounts through Discord slash commands.

## Features
- `/balance` - Check your bank balance and wallet (auto-creates account if needed)
- `/deposit <amount>` - Deposit money from wallet to bank
- `/withdraw <amount>` - Withdraw money from bank to wallet

## Project Structure
- `bot.py` - Main bot code with Discord commands and banking logic
- `bank.json` - Sample bank data (actual data stored in `~/bot/bank.json`)
- `requirements.txt` - Python dependencies

## Configuration
- **DISCORD_TOKEN** - Bot token from Discord Developer Portal (stored as secret)

## Technical Notes
- Built with discord.py library
- Uses slash commands (app_commands)
- Bank data persists to JSON file at `$HOME/bot/bank.json`
- Default account: 1000 in bank, 0 in wallet, level 1

## Running
The bot runs via the "Discord Bot" workflow which executes `python bot.py`.
