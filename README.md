# Discord Message Summarizer Bot

A personal Discord bot that summarizes messages in channels using AI (OpenRouter API). Designed for free hosting on Oracle Cloud.

## Features

- `/summarize` - Summarize recent messages in a channel
- `/summarize_help` - Get help with the summarize command
- Customizable summary length (short, medium, long)
- Flexible message selection (by count or time range)
- Powered by OpenRouter API (supports Claude, GPT-4, and more)

## Commands

### `/summarize [options]`

Options:
- `count` - Number of messages to summarize (1-100, default: 50)
- `hours` - Summarize messages from the last X hours
- `length` - Summary length: short, medium, or long (default: medium)

Examples:
- `/summarize` - Summarize last 50 messages
- `/summarize count:100` - Summarize last 100 messages
- `/summarize hours:24` - Summarize messages from last 24 hours
- `/summarize length:short` - Get a brief summary
- `/summarize count:50 length:long` - Combine options

### `/summarize_help`
Shows detailed help information for the bot.

## Prerequisites

- Python 3.11 or higher
- Discord account
- OpenRouter API key (free tier available)
- Oracle Cloud account (free tier)

## Setup Instructions

### 1. Clone or Download

```bash
git clone <repository-url>
cd DiscordBot
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your credentials:
   - `DISCORD_TOKEN` - Your Discord bot token (from Developer Portal)
   - `OPENROUTER_API_KEY` - Your OpenRouter API key
   - Optional: Adjust other settings as needed

### 5. Run the Bot

```bash
python bot.py
```

The bot will connect to Discord and sync slash commands. This may take up to an hour for global commands.

## Getting API Keys

### Discord Bot Token

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" and give it a name
3. Go to "Bot" section and click "Add Bot"
4. Click "Reset Token" and copy the token
5. Go to "OAuth2" → "URL Generator"
6. Select scopes: `bot`, `applications.commands`
7. Select permissions: `Send Messages`, `Read Message History`, `Use Slash Commands`
8. Use the generated URL to invite the bot to your server

### OpenRouter API Key

1. Go to [OpenRouter](https://openrouter.ai/)
2. Create an account or log in
3. Go to [Keys](https://openrouter.ai/keys)
4. Create a new API key
5. Copy the key (you'll need this for the `.env` file)

## Deployment to Oracle Cloud (Free Tier)

### 1. Create Oracle Cloud Account

1. Go to [Oracle Cloud](https://www.oracle.com/cloud/)
2. Sign up for free tier (no credit card required for free tier)

### 2. Create VM Instance

1. In Oracle Cloud Console, go to "Compute" → "Instances"
2. Click "Create Instance"
3. Configure:
   - Name: `discord-bot` (or your choice)
   - Image: Ubuntu 22.04
   - Shape: VM.Standard.A1.Flex (ARM - Always Free)
   - OCPUs: 1 (Always Free: up to 4 OCPUs)
   - Memory: 6 GB (Always Free: up to 24 GB)
4. Add SSH key (generate one if needed)
5. Click "Create"

### 3. Configure Security Rules

1. Go to "Networking" → "Virtual Cloud Networks"
2. Click on your VCN
3. Click on your subnet
4. Click "Security Lists" → your security list
5. Add Ingress Rule:
   - Source: 0.0.0.0/0
   - Destination Port: 22 (SSH)
6. Click "Add Ingress Rules"

### 4. Connect to Your VM

```bash
ssh -i /path/to/your/key.pem ubuntu@<your-instance-ip>
```

### 5. Setup Server

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and git
sudo apt install python3.11 python3.11-venv git -y

# Clone your repository (or upload files)
git clone <your-repo-url>
cd DiscordBot

# Setup virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file with your credentials
nano .env
# (paste your environment variables and save)

# Test the bot
python bot.py
# Press Ctrl+C to stop
```

### 6. Create Systemd Service (Auto-restart)

Create service file:
```bash
sudo nano /etc/systemd/system/discord-bot.service
```

Add this content:
```ini
[Unit]
Description=Discord Summarizer Bot
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/DiscordBot
Environment=PATH=/home/ubuntu/DiscordBot/venv/bin
ExecStart=/home/ubuntu/DiscordBot/venv/bin/python bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start the service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable discord-bot
sudo systemctl start discord-bot

# Check status
sudo systemctl status discord-bot

# View logs
sudo journalctl -u discord-bot -f
```

### 7. Update Bot (Future Updates)

```bash
cd ~/DiscordBot
git pull
sudo systemctl restart discord-bot
```

## Project Structure

```
DiscordBot/
├── bot.py              # Main bot file
├── config.py           # Configuration management
├── utils/
│   ├── __init__.py
│   └── summarizer.py   # Summarization logic
├── requirements.txt    # Python dependencies
├── .env.example        # Environment template
├── .env                # Your credentials (not in git)
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## Configuration Options

All configuration is done via environment variables in `.env`:

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `DISCORD_TOKEN` | Yes | - | Your Discord bot token |
| `OPENROUTER_API_KEY` | Yes | - | Your OpenRouter API key |
| `DISCORD_GUILD_ID` | No | - | Server ID for faster command sync |
| `OPENROUTER_BASE_URL` | No | `https://openrouter.ai/api/v1` | OpenRouter API URL |
| `DEFAULT_MODEL` | No | `anthropic/claude-3.5-sonnet` | LLM model to use |
| `MAX_TOKENS` | No | `1000` | Max tokens for summary |
| `MAX_MESSAGES_PER_REQUEST` | No | `100` | Max messages to process |
| `DEFAULT_MESSAGE_COUNT` | No | `50` | Default messages to summarize |

## Troubleshooting

### Bot not responding to commands
- Check bot has proper permissions in Discord
- Verify bot is online in Discord
- Wait up to an hour for slash commands to sync globally
- Check logs: `sudo journalctl -u discord-bot -f`

### "Configuration errors" on startup
- Verify `.env` file exists and has correct values
- Check for typos in environment variable names
- Ensure no extra spaces in values

### API errors
- Verify OpenRouter API key is valid
- Check you have credits/usage available
- Try a different model in `.env`

### Bot crashes or won't start
- Check Python version: `python3 --version` (need 3.11+)
- Verify all dependencies installed: `pip install -r requirements.txt`
- Check logs for error messages

## License

This project is for personal use. Feel free to modify and adapt.

## Support

For issues or questions:
1. Check the Troubleshooting section
2. Review logs: `sudo journalctl -u discord-bot -f`
3. Verify all configuration in `.env`