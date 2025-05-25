import os
import logging
from dotenv import load_dotenv
from transcription import transcribe_audio
from agent import process_command
from utils import setup_logging, speak_text
from calendar_tools import CalendarManager

# Setup logging
setup_logging()

# Load environment variables
load_dotenv()

def main():
    print("Welcome to Voice Calendar Assistant!")
    print("Say your command or type 'exit' to quit.")
    
    calendar_manager = CalendarManager()
    
    while True:
        try:
            # Get audio input
            print("\nListening...")
            audio_file = input("Enter path to audio file or type 'exit': ")
            
            if audio_file.lower() == 'exit':
                break
                
            # Transcribe audio
            transcription = transcribe_audio(audio_file)
            if not transcription:
                print("Sorry, I couldn't understand that.")
                continue
                
            logging.info(f"Transcription: {transcription}")
            
            # Process command
            response = process_command(transcription, calendar_manager)
            print(f"\n{response}")
            
            # Optional: Speak response
            speak_text(response)
            
        except Exception as e:
            logging.error(f"Error in main loop: {str(e)}")
            print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
