import openai
from typing import List, Dict
import config

class MessageSummarizer:
    """Handles message summarization using OpenRouter API."""
    
    def __init__(self):
        """Initialize the OpenAI client with OpenRouter configuration."""
        self.client = openai.OpenAI(
            api_key=config.OPENROUTER_API_KEY,
            base_url=config.OPENROUTER_BASE_URL
        )
        self.model = config.DEFAULT_MODEL
    
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
    
    def create_summarization_prompt(self, messages_text: str, summary_length: str = "medium") -> str:
        """Create the prompt for summarization.
        
        Args:
            messages_text: Formatted messages text
            summary_length: Length of summary (short, medium, long)
            
        Returns:
            Formatted prompt string
        """
        length_instructions = {
            "short": "Provide a brief 2-3 sentence summary",
            "medium": "Provide a concise summary in 1-2 paragraphs",
            "long": "Provide a detailed summary covering all key points"
        }
        
        instruction = length_instructions.get(summary_length, length_instructions["medium"])
        
        prompt = f"""Please summarize the following Discord channel conversation. {instruction}.

Focus on:
- Main topics discussed
- Key decisions or conclusions
- Important information shared
- Overall sentiment/tone

Conversation:
{messages_text}

Summary:"""
        
        return prompt
    
    async def summarize_messages(self, messages: List[Dict], summary_length: str = "medium") -> str:
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
            
            # Call OpenRouter API
            response = self.client.chat.completions.create(
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
                temperature=0.3  # Lower temperature for more focused summaries
            )
            
            # Extract and return summary
            summary = response.choices[0].message.content
            return summary.strip()
            
        except openai.APIError as e:
            raise Exception(f"OpenRouter API error: {str(e)}")
        except Exception as e:
            raise Exception(f"Summarization failed: {str(e)}")