# Discord Bot with Message Summarization - Project Plan

## Overview
Create a personal Discord bot with message summarization capabilities using Python, OpenRouter API, and Oracle Cloud free tier hosting.

## Technology Stack
- **Language:** Python 3.11+
- **Discord Library:** discord.py
- **LLM API:** OpenRouter (via OpenAI-compatible API)
- **Hosting:** Oracle Cloud Free Tier ARM instance
- **Deployment:** Systemd service

## Project Structure
```
DiscordBot/
├── bot.py              # Main bot file
├── cogs/
│   └── summarizer.py   # Summarization command (optional organization)
├── utils/
│   ├── __init__.py
│   └── summarizer.py   # Summarization logic
├── config.py           # Configuration management
├── requirements.txt    # Python dependencies
├── .env                # Environment variables
├── bot.service         # Systemd service file
└── README.md
```

## Implementation Phases

### Phase 1: Setup (1-2 hours)
1. **Create Discord Application**
   - Go to Discord Developer Portal
   - Create new application
   - Add bot and get token
   - Set up OAuth2 permissions

2. **Set up Python Project**
   - Create virtual environment
   - Install discord.py, openai, python-dotenv
   - Create basic project structure

3. **Implement Core Bot**
   - Bot initialization and event handlers
   - Command prefix or slash commands
   - Basic error handling

### Phase 2: Summarization Feature (2-3 hours)
1. **Message Fetching**
   - Fetch messages from channel (with pagination for long histories)
   - Format messages for LLM input

2. **OpenRouter Integration**
   - Configure OpenAI client with OpenRouter base URL
   - Create summarization prompt
   - Handle API responses and errors

3. **Command Implementation**
   - `/summarize` slash command (modern approach)
   - Options for message count or time range
   - Response formatting

### Phase 3: Deployment (1-2 hours)
1. **Oracle Cloud VM Setup**
   - Launch ARM instance (Ubuntu 22.04 recommended)
   - Configure security rules (SSH access)
   - Connect via SSH

2. **Deploy Bot**
   - Upload code (git or SCP)
   - Set up Python environment
   - Create systemd service for auto-restart
   - Start and enable service

3. **Testing & Verification**
   - Test bot in Discord
   - Verify summarization works
   - Check auto-restart functionality

## Key Features
- `/summarize [count]` - Summarize last X messages
- `/summarize [hours]` - Summarize messages from last X hours
- Configurable summary length
- Error handling for API limits
- Channel-specific (only works in designated channels if desired)

## Estimated Costs
- **Oracle Cloud Free Tier:** $0/month (always free)
- **OpenRouter API:** Pay-per-use (varies by model, very affordable)
- **Total:** Essentially free for light usage

## Deployment Method
- **Systemd service** - Simple, reliable, auto-restarts on failure
- **Git-based deployment** - Easy updates with `git pull`
- **Virtual environment** - Isolates dependencies

## Python vs Node.js Trade-offs

**Python Advantages:**
- Easier for beginners
- Excellent OpenRouter API support with `openai` library
- `discord.py` is very well-documented and beginner-friendly
- Simpler syntax and easier debugging

**Python Disadvantages:**
- Slightly slower than Node.js (but negligible for a bot)
- May use slightly more memory (but still well within Oracle Cloud free tier)

**Conclusion:** Python is an excellent choice for this project.

## Next Steps
1. Set up Discord application in Developer Portal
2. Implement core bot structure
3. Add summarization functionality with OpenRouter
4. Deploy to Oracle Cloud free tier
5. Test and verify all functionality