import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime, timedelta
import asyncio
from typing import Optional

import config
from utils.summarizer import MessageSummarizer

# Validate configuration on startup
config.validate_config()

# Set up intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Create bot instance
bot = commands.Bot(command_prefix='!', intents=intents)

# Initialize summarizer
summarizer = MessageSummarizer()

@bot.event
async def on_ready():
    """Called when the bot is ready and connected to Discord."""
    print(f'{bot.user} has connected to Discord!')
    print(f'Bot is in {len(bot.guilds)} guild(s)')
    
    # Sync slash commands
    try:
        synced = await bot.tree.sync()
        print(f'Synced {len(synced)} command(s)')
    except Exception as e:
        print(f'Failed to sync commands: {e}')

@bot.tree.command(name='summarize', description='Summarize recent messages in this channel')
@app_commands.describe(
    count='Number of messages to summarize (default: 50)',
    hours='Summarize messages from the last X hours (alternative to count)',
    length='Summary length: short, medium, or long (default: medium)'
)
async def summarize_command(
    interaction: discord.Interaction,
    count: Optional[int] = None,
    hours: Optional[float] = None,
    length: Optional[str] = 'medium'
):
    """Slash command to summarize messages in the current channel."""
    # Defer response since summarization may take time
    await interaction.response.defer()
    
    try:
        # Validate length parameter
        valid_lengths = ['short', 'medium', 'long']
        if length and length.lower() not in valid_lengths:
            await interaction.followup.send(
                f"Invalid length '{length}'. Valid options: {', '.join(valid_lengths)}",
                ephemeral=True
            )
            return
        
        summary_length = length.lower() if length else 'medium'
        
        # Determine how many messages to fetch
        if hours:
            # Summarize messages from last X hours
            after_time = datetime.utcnow() - timedelta(hours=hours)
            messages = []
            async for message in interaction.channel.history(after=after_time, limit=config.MAX_MESSAGES_PER_REQUEST):
                if not message.author.bot:  # Skip bot messages
                    messages.append({
                        'author': str(message.author.display_name),
                        'content': message.content,
                        'timestamp': message.created_at.strftime('%Y-%m-%d %H:%M')
                    })
            
            if not messages:
                await interaction.followup.send(
                    f"No messages found in the last {hours} hour(s).",
                    ephemeral=True
                )
                return
            
            time_description = f"last {hours} hour(s)"
            
        else:
            # Summarize last X messages
            message_count = count if count else config.DEFAULT_MESSAGE_COUNT
            message_count = min(message_count, config.MAX_MESSAGES_PER_REQUEST)
            
            messages = []
            async for message in interaction.channel.history(limit=message_count):
                if not message.author.bot:  # Skip bot messages
                    messages.append({
                        'author': str(message.author.display_name),
                        'content': message.content,
                        'timestamp': message.created_at.strftime('%Y-%m-%d %H:%M')
                    })
            
            if not messages:
                await interaction.followup.send(
                    "No messages found to summarize.",
                    ephemeral=True
                )
                return
            
            time_description = f"last {len(messages)} messages"
        
        # Generate summary
        summary = await summarizer.summarize_messages(messages, summary_length)
        
        # Create embed for nice formatting
        embed = discord.Embed(
            title="📝 Channel Summary",
            description=summary,
            color=discord.Color.blue(),
            timestamp=datetime.utcnow()
        )
        embed.set_footer(text=f"Summarized {time_description} • Length: {summary_length}")
        
        await interaction.followup.send(embed=embed)
        
    except Exception as e:
        error_message = f"An error occurred while summarizing: {str(e)}"
        await interaction.followup.send(error_message, ephemeral=True)
        print(f"Summarize command error: {e}")

@bot.tree.command(name='summarize_help', description='Get help with the summarize command')
async def help_command(interaction: discord.Interaction):
    """Show help information for the summarize command."""
    embed = discord.Embed(
        title="📚 Summarize Command Help",
        description="Summarize messages in the current channel using AI",
        color=discord.Color.green()
    )
    
    embed.add_field(
        name="Usage",
        value=(
            "`/summarize` - Summarize last 50 messages\n"
            "`/summarize count:100` - Summarize last 100 messages\n"
            "`/summarize hours:24` - Summarize messages from last 24 hours\n"
            "`/summarize length:short` - Get a brief summary\n"
            "`/summarize count:50 length:long` - Combine options"
        ),
        inline=False
    )
    
    embed.add_field(
        name="Options",
        value=(
            "**count**: Number of messages (1-100, default: 50)\n"
            "**hours**: Time range in hours (alternative to count)\n"
            "**length**: Summary length - short, medium, or long"
        ),
        inline=False
    )
    
    embed.add_field(
        name="Examples",
        value=(
            "`/summarize` - Quick summary of recent chat\n"
            "`/summarize hours:12 length:short` - Brief summary of last 12 hours\n"
            "`/summarize count:100 length:long` - Detailed summary of 100 messages"
        ),
        inline=False
    )
    
    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.event
async def on_command_error(ctx, error):
    """Handle command errors."""
    if isinstance(error, commands.CommandNotFound):
        return
    print(f"Command error: {error}")

def main():
    """Main entry point for the bot."""
    print("Starting Discord bot...")
    bot.run(config.DISCORD_TOKEN)

if __name__ == '__main__':
    main()