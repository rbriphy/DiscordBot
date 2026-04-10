import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Discord Configuration
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
DISCORD_GUILD_ID = os.getenv('DISCORD_GUILD_ID')  # Optional: specific server ID

# OpenRouter Configuration
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
OPENROUTER_BASE_URL = os.getenv('OPENROUTER_BASE_URL', 'https://openrouter.ai/api/v1')

# Model Configuration
# These are hardcoded in config so you can safely commit them to git
# Environment variables will NOT override these values
DEFAULT_MODEL = 'openai/gpt-oss-120b:free'
MAX_TOKENS = int(os.getenv('MAX_TOKENS', '1000'))

# Summarization Settings
MAX_MESSAGES_PER_REQUEST = int(os.getenv('MAX_MESSAGES_PER_REQUEST', '100'))
DEFAULT_MESSAGE_COUNT = int(os.getenv('DEFAULT_MESSAGE_COUNT', '50'))
SUMMARY_TEMPERATURE = float(os.getenv('SUMMARY_TEMPERATURE', '0.3'))

def validate_config():
    """Validate that all required configuration is present."""
    errors = []
    
    if not DISCORD_TOKEN:
        errors.append("DISCORD_TOKEN is required")
    
    if not OPENROUTER_API_KEY:
        errors.append("OPENROUTER_API_KEY is required")
    
    if errors:
        raise ValueError("Configuration errors:\n" + "\n".join(f"  - {e}" for e in errors))
    
    return True