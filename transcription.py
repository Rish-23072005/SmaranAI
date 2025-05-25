import whisper
import logging
from typing import Optional

def transcribe_audio(audio_file: str) -> Optional[str]:
    """
    Transcribe audio file using Groq Whisper API.
    Supports both Hindi and English languages.
    
    Args:
        audio_file: Path to the audio file
        
    Returns:
        Transcribed text or None if transcription fails
    """
    try:
        # Load the model
        model = whisper.load_model("base")
        
        # Transcribe audio
        result = model.transcribe(audio_file, language=None)
        
        # Get the transcription
        transcription = result["text"]
        
        # Detect language and log
        detected_lang = result["language"]
        logging.info(f"Detected language: {detected_lang}")
        
        return transcription.strip()
        
    except Exception as e:
        logging.error(f"Error transcribing audio: {str(e)}")
        return None
