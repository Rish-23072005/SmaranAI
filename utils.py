import logging
import os
from datetime import datetime
import dateparser
import parsedatetime
from typing import Optional
import pyttsx3

def setup_logging():
    """Setup logging configuration."""
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(os.path.join(log_dir, 'calendar_agent.log')),
            logging.StreamHandler()
        ]
    )

def parse_date_time(text: str) -> Optional[datetime]:
    """
    Parse date and time from natural language text.
    Uses both dateparser and parsedatetime for better accuracy.
    
    Args:
        text: Natural language text containing date/time
        
    Returns:
        Parsed datetime object or None if parsing fails
    """
    try:
        # Try dateparser first
        parsed_date = dateparser.parse(text)
        if parsed_date:
            return parsed_date
            
        # Try parsedatetime if dateparser fails
        cal = parsedatetime.Calendar()
        time_struct, parse_status = cal.parse(text)
        if parse_status:
            return datetime(*time_struct[:6])
            
        return None
        
    except Exception as e:
        logging.error(f"Error parsing date/time: {str(e)}")
        return None

def speak_text(text: str):
    """
    Convert text to speech using pyttsx3.
    
    Args:
        text: Text to be converted to speech
    """
    try:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        logging.error(f"Error in text-to-speech: {str(e)}")
