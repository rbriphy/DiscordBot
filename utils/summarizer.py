import openai
import json
import logging
import os
from typing import List, Dict
import config

logger = logging.getLogger(__name__)

class MessageSummarizer:
    """Handles message summarization using OpenRouter API."""
    
    def __init__(self):
        """Initialize the async OpenAI client with OpenRouter configuration."""
        self.client = openai.AsyncOpenAI(
            api_key=config.OPENROUTER_API_KEY,
            base_url=config.OPENROUTER_BASE_URL,
            timeout=30.0  # 30 second timeout for API calls
        )
        self.model = config.DEFAULT_MODEL
        self.username_mapping = self._load_username_mapping()
    
    def _load_username_mapping(self) -> Dict[str, str]:
        """Load username to nickname mapping from JSON file.
        
        Returns:
            Dictionary mapping usernames to nicknames
        """
        try:
            # Get the directory where this script is located
            script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            json_path = os.path.join(script_dir, 'usernames.json')
            with open(json_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning("usernames.json not found, username mapping disabled")
            return {}
        except json.JSONDecodeError:
            logger.warning("Invalid JSON in usernames.json, username mapping disabled")
            return {}
    
    def format_messages_for_summary(self, messages: List[Dict]) -> str:
        """Format Discord messages for summarization prompt.
        
        Args:
            messages: List of message dictionaries with 'author', 'content', 'timestamp'
            
        Returns:
            Formatted string of messages
        """
        formatted = []
        for msg in messages:
            author = msg.get('author', 'Unknown')
            content = msg.get('content', '')
            timestamp = msg.get('timestamp', '')
            
            if content:  # Only include messages with content
                formatted.append(f"[{timestamp}] {author}: {content}")
        
        return "\n".join(formatted)
    
    def create_summarization_prompt(self, messages_text: str, summary_length: str = "short") -> str:
        """Create the prompt for summarization.
        
        Args:
            messages_text: Formatted messages text
            summary_length: Length of summary (short or long)
            
        Returns:
            Formatted prompt string
        """
        length_instructions = {
            "short": "Write 1-2 casual sentences summarizing what happened",
            "long": "Write a brief casual summary of the conversation"
        }
        
        instruction = length_instructions.get(summary_length, length_instructions["short"])
        
        # Build username cheat sheet from loaded mapping
        cheat_sheet = ""
        if self.username_mapping:
            cheat_sheet_lines = []
            for username, nickname in self.username_mapping.items():
                cheat_sheet_lines.append(f"({username}:{nickname})")
            cheat_sheet = "\n".join(cheat_sheet_lines)
        
        prompt = f"""Summarize this Discord conversation. {instruction}. Use the actual names from the messages. Use plain language without sounding like a business report. Don't analyze sentiment or tone - just describe what people talked about.

        Username Cheat Sheet Format: (Username:Nickname) 
        Refer to users as their Nickname when performing summaries. The Username is what is displayed in chat.
{cheat_sheet}

Messages:
{messages_text}

Summary:"""
        
        return prompt
    
    async def summarize_messages(self, messages: List[Dict], summary_length: str = "short") -> str:
        """Summarize a list of Discord messages.
        
        Args:
            messages: List of message dictionaries
            summary_length: Desired summary length
            
        Returns:
            Summary text
            
        Raises:
            Exception: If API call fails
        """
        try:
            # Format messages
            messages_text = self.format_messages_for_summary(messages)
            
            if not messages_text.strip():
                return "No messages found to summarize."
            
            # Create prompt
            prompt = self.create_summarization_prompt(messages_text, summary_length)
            
            # Call OpenRouter API (async)
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that summarizes Discord conversations clearly and concisely."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=config.MAX_TOKENS,
                temperature=config.SUMMARY_TEMPERATURE
            )
            
            # Extract and return summary
            if not response.choices:
                return "Unable to generate summary."
            summary = response.choices[0].message.content
            if summary is None:
                return "Unable to generate summary."
            return summary.strip()
            
        except openai.APIError as e:
            raise Exception(f"OpenRouter API error: {str(e)}")
        except Exception as e:
            raise Exception(f"Summarization failed: {str(e)}")