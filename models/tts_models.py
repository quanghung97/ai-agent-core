from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs
from config.settings import get_settings
from typing import Optional, Dict, Any
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class ElevenLabsModels(Enum):
    """Available ElevenLabs TTS models"""
    # Flagship Models - Highest Quality
    MULTILINGUAL_V2 = "eleven_multilingual_v2"  # Most lifelike, emotionally rich
    MULTILINGUAL_V1 = "eleven_multilingual_v1"  # Legacy multilingual model
    
    # Flash Models - Low Latency
    FLASH_V2_5 = "eleven_flash_v2_5"  # Fastest model with 32 languages support
    FLASH_V2 = "eleven_flash_v2"  # Fast model with good quality
    
    # English Only Models
    MONOLINGUAL_V1 = "eleven_monolingual_v1"  # English-only high quality
    ENGLISH_V1 = "eleven_english_v1"  # Alternative English model
    
    # Turbo Models - Balance of speed and quality
    TURBO_V2_5 = "eleven_turbo_v2_5"  # Fast with language enforcement support
    TURBO_V2 = "eleven_turbo_v2"  # Balanced speed and quality

    @classmethod
    def get_description(cls, model):
        """Get description for a model"""
        descriptions = {
            cls.MULTILINGUAL_V2: "Most lifelike, emotionally rich model. Best for voiceovers, audiobooks, content creation. Supports 32 languages.",
            cls.MULTILINGUAL_V1: "Legacy multilingual model with good quality.",
            cls.FLASH_V2_5: "Fastest model (~75ms latency) for real-time AI applications. Supports 32 languages including Vietnamese, Hungarian, Norwegian.",
            cls.FLASH_V2: "Fast model with good quality, optimized for low latency.",
            cls.MONOLINGUAL_V1: "High-quality English-only model.",
            cls.ENGLISH_V1: "Alternative English-only model.",
            cls.TURBO_V2_5: "Fast model with language enforcement support.",
            cls.TURBO_V2: "Balanced speed and quality model."
        }
        return descriptions.get(model, "No description available")
    
    @classmethod
    def get_recommended_for_use_case(cls, use_case: str):
        """Get recommended model for specific use case"""
        recommendations = {
            "real_time": cls.FLASH_V2_5,
            "conversational_ai": cls.FLASH_V2_5,
            "voiceover": cls.MULTILINGUAL_V2,
            "audiobook": cls.MULTILINGUAL_V2,
            "content_creation": cls.MULTILINGUAL_V2,
            "english_only": cls.MONOLINGUAL_V1,
            "balanced": cls.TURBO_V2_5,
            "fastest": cls.FLASH_V2_5,
            "highest_quality": cls.MULTILINGUAL_V2
        }
        return recommendations.get(use_case.lower(), cls.MULTILINGUAL_V2)

class TextToSpeechModel:
    def __init__(self):
        self.settings = get_settings()
        self.api_key = self.settings.ELEVENLABS_API_KEY
        if not self.api_key:
            raise ValueError("ELEVENLABS_API_KEY not found in environment variables")
        self.client = ElevenLabs(api_key=self.api_key)

    async def generate_speech(
        self, 
        text: str,
        voice_id: str = "21m00Tcm4TlvDq8ikWAM",
        model: ElevenLabsModels = ElevenLabsModels.FLASH_V2_5,
        voice_settings: Optional[Dict[str, Any]] = None
    ) -> bytes:
        """Generate speech from text using ElevenLabs v2.1.0 SDK"""
        try:
            # Create VoiceSettings object if voice_settings dict is provided
            settings = None
            if voice_settings:
                settings = VoiceSettings(
                    stability=voice_settings.get("stability", 0.7),
                    similarity_boost=voice_settings.get("similarity_boost", 0.7),
                    style=voice_settings.get("style", 0.0),
                    use_speaker_boost=getattr(voice_settings, 'use_speaker_boost', False),
                    speed=voice_settings.get("speed", 1.0)
                )

            # Generate speech using the synchronous method
            response = self.client.text_to_speech.convert(
                voice_id=voice_id,
                model_id=model.value,
                text=text,
                voice_settings=settings
            )

            # Convert response to bytes
            audio_bytes = b"".join(response)
            return audio_bytes

        except Exception as e:
            logger.error(f"Text-to-speech generation failed: {str(e)}")
            raise
