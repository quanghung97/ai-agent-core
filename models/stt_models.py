from typing import Dict, Any
from openai import AsyncOpenAI
from config.settings import get_settings
import aiohttp
import logging

logger = logging.getLogger(__name__)

class SpeechToTextModel:
    """Wrapper for OpenAI Whisper API"""
    
    def __init__(self):
        self.settings = get_settings()
        self.client = AsyncOpenAI(api_key=self.settings.OPENAI_API_KEY)
        self.model = "whisper-1"
        
    async def transcribe(self, audio_url: str) -> Dict[str, Any]:
        """Transcribe audio file using Whisper API"""
        try:
            # Download audio file
            async with aiohttp.ClientSession() as session:
                async with session.get(audio_url) as response:
                    audio_data = await response.read()
            
            # Transcribe using Whisper
            response = await self.client.audio.transcriptions.create(
                model=self.model,
                file=("audio.mp3", audio_data),
                response_format="verbose_json"
            )
            
            return {
                "text": response.text,
                "language": response.language,
                "duration": response.duration,
                "segments": response.segments
            }
            
        except Exception as e:
            logger.error(f"Transcription failed: {str(e)}")
            raise Exception(f"Transcription failed: {str(e)}")
