# Instagram Story Hunter Telegram Bot

A Python bot that monitors Instagram stories for specified accounts and sends new story updates to a Telegram chat.

## Features
- Monitors Instagram stories for any number of accounts (listed in `accounts.txt`)
- Sends new story notifications to a Telegram chat
- Avoids duplicate notifications
- Logs activity to `log.txt`

## Requirements
- Python 3.8+
- Telegram bot token (from [@BotFather](https://t.me/BotFather))
- Telegram user ID (your own Telegram numeric ID)

## Installation
1. **Clone the repository:**
   ```bash
   git clone https://github.com/okoyausman/instagram-story-hunter.git
   cd instagram-story-hunter
   ```
2. **Install dependencies:**
   ```bash
   pip install python-telegram-bot requests curl_cffi
   ```

## Configuration
1. **Environment Variables:**
   - Copy `env.example` to `.env`:
     ```bash
     cp env.example .env
     ```
   - Edit `.env` and fill in your actual `TELEGRAM_BOT_TOKEN` and `TELEGRAM_USER_ID`.
2. **Instagram Accounts:**
   - Add one Instagram username per line in `accounts.txt` (create the file if it doesn't exist).

## Usage
Run the bot with:
```bash
python bot.py
```

- The bot will check for new stories every 10 minutes.
- When a new story is found, it sends a message to the configured Telegram user.
- Approving a story triggers the custom processing function in `bot.py`.

## Logging
- All actions and errors are logged to `log.txt`.

## Credits
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
- [anonstories.com](https://anonstories.com/) for the Instagram story API

## License
MIT 