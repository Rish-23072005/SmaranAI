from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers import pipeline
import logging
from datetime import datetime
import dateparser # type: ignore
from typing import Optional
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class CalendarAgent:
    def __init__(self):
        """Initialize the Hugging Face agent with system prompt."""
        # Load the model and tokenizer using Hugging Face token
        self.model_name = "microsoft/DialoGPT-medium"  # Good for conversation
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_name,
            use_auth_token=os.getenv("HF_API_KEY")
        )
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            use_auth_token=os.getenv("HF_API_KEY")
        )
        
        self.system_prompt = """
        You are a helpful calendar assistant that can process voice commands in Hindi and English.
        You can understand and extract date/time information from natural language.
        
        Examples:
        - "I have a meeting tomorrow at 3 PM"
        - "Mujhe kal subah 10 baje doctor appointment set karna hai"
        
        Extract the following information:
        1. Event type (meeting, appointment, etc.)
        2. Date and time (in ISO format)
        3. Any additional details
        """

    def process_command(self, command: str, calendar_manager) -> str:
        """
        Process a voice command and execute the appropriate calendar action.
        
        Args:
            command: Transcribed voice command
            calendar_manager: CalendarManager instance
            
        Returns:
            Response message to user
        """
        try:
            # Parse date/time from command
            parsed_date = dateparser.parse(command)
            if not parsed_date:
                return "Could not understand the date/time. Please clarify."
                
            # Create conversation context
            context = f"{self.system_prompt}\n\nCommand: {command}\nParsed Date: {parsed_date.isoformat()}"
            
            # Generate response using Hugging Face pipeline
            chat = pipeline("conversational", model=self.model, tokenizer=self.tokenizer)
            response = chat(context)[0]["generated_text"]
            
            # Extract action and details
            action = self._extract_action(response)
            
            # Execute calendar action
            result = self._execute_calendar_action(action, calendar_manager)
            return result
            
        except Exception as e:
            logging.error(f"Error processing command: {str(e)}")
            return f"An error occurred: {str(e)}"

    def _extract_action(self, response: str) -> dict:
        """Extract action details from model response."""
        try:
            # Simple parsing of response
            # This could be made more sophisticated with regex or NLP
            if "create event" in response.lower():
                return {
                    "action": "create",
                    "details": self._parse_event_details(response)
                }
            elif "show events" in response.lower():
                return {
                    "action": "fetch"
                }
            return {}
        except Exception as e:
            logging.error(f"Error extracting action: {str(e)}")
            return {}

    def _parse_event_details(self, text: str) -> dict:
        """Parse event details from text."""
        try:
            # Simple parsing - this could be enhanced with NLP
            details = {}
            if "meeting" in text.lower():
                details["summary"] = "Meeting"
            elif "appointment" in text.lower():
                details["summary"] = "Appointment"
            return details
        except Exception as e:
            logging.error(f"Error parsing event details: {str(e)}")
            return {}

    def _execute_calendar_action(self, action: dict, calendar_manager) -> str:
        """Execute the appropriate calendar action."""
        try:
            if action.get("action") == "create":
                return calendar_manager.create_event(action["details"])
            elif action.get("action") == "fetch":
                return calendar_manager.get_upcoming_events()
            return "Action not recognized"
        except Exception as e:
            logging.error(f"Error executing action: {str(e)}")
            return f"Failed to execute action: {str(e)}"

def process_command(command: str, calendar_manager) -> str:
    agent = CalendarAgent()
    return agent.process_command(command, calendar_manager)
