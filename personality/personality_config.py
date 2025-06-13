from pydantic import BaseModel, Field
from typing import List, Optional, Dict

class SpeechPatterns(BaseModel):
    tone: str = "neutral"
    vocabulary: str = "standard"
    catchphrases: List[str] = []

class ResponseStyle(BaseModel):
    detail_level: str = "balanced"
    emotional_expressiveness: str = "moderate"

class BehavioralSettings(BaseModel):
    speech_patterns: SpeechPatterns
    response_style: ResponseStyle

class Appearance(BaseModel):
    height: str 
    build: str
    hair: str
    eyes: str
    style: str
    distinguishing_features: List[str] = []

class Background(BaseModel):
    origin: str
    experiences: List[str] = []
    education: Optional[str] = None
    occupation: Optional[str] = None

class PersonalityTraits(BaseModel):
    friendliness: float = Field(default=0.5, ge=0.0, le=1.0)
    humor: float = Field(default=0.5, ge=0.0, le=1.0)
    formality: float = Field(default=0.5, ge=0.0, le=1.0)
    creativity: float = Field(default=0.5, ge=0.0, le=1.0)
    detail_oriented: float = Field(default=0.5, ge=0.0, le=1.0)
class Personality(BaseModel):
    traits: PersonalityTraits
    values: List[str] = []
    fears: List[str] = []
    motivations: List[str] = []

class WorldContext(BaseModel):
    setting: str = "Cyberpunk dystopia, 2087"
    technology_level: str = "Advanced AI, neural implants, quantum computing"
    social_structure: str = "Corporate oligarchy, underground resistance"

class PersonalityConfig(BaseModel):
    name: str
    gender: str
    age: int = Field(ge=0)
    personality: Personality
    interests: List[str] = []
    communication_style: str
    language: str = "en"
    artistic_style: str
    appearance: Appearance
    background: Background
    behavioral_settings: BehavioralSettings
    world_context: WorldContext
    knowledge_base: Dict[str, List[str]] = {}
    
    def generate_prompt(self) -> str:
        return f"""You are {self.name}, a {self.age}-year-old {self.gender} living in {self.world_context.setting}.

CHARACTER IDENTITY:
- Background: {self.background.origin}
- Occupation: {self.background.occupation or 'Not specified'}
- Education: {self.background.education or 'Not specified'}
- Key experiences: {', '.join(self.background.experiences)}

PERSONALITY & BEHAVIOR:
- Values: {', '.join(self.personality.values)}
- Fears: {', '.join(self.personality.fears)}
- Motivations: {', '.join(self.personality.motivations)}
- Interests: {', '.join(self.interests)}

APPEARANCE:
- Physical: {self.appearance.height}, {self.appearance.build}
- Features: {self.appearance.hair}, {self.appearance.eyes}
- Style: {self.appearance.style}
- Distinctive: {', '.join(self.appearance.distinguishing_features)}

COMMUNICATION STYLE:
- Tone: {self.behavioral_settings.speech_patterns.tone}
- Vocabulary: {self.behavioral_settings.speech_patterns.vocabulary}
- Catchphrases: {', '.join(self.behavioral_settings.speech_patterns.catchphrases)}
- Detail Level: {self.behavioral_settings.response_style.detail_level}
- Emotional Expression: {self.behavioral_settings.response_style.emotional_expressiveness}

PERSONALITY TRAITS (0-1 scale):
- Friendliness: {self.personality.traits.friendliness}
- Humor: {self.personality.traits.humor}
- Formality: {self.personality.traits.formality}
- Creativity: {self.personality.traits.creativity}
- Detail-oriented: {self.personality.traits.detail_oriented}

WORLD CONTEXT:
- Setting: {self.world_context.setting}
- Technology Level: {self.world_context.technology_level}
- Social Structure: {self.world_context.social_structure}

BEHAVIORAL RULES:
1. Stay in character at all times
2. Use your specific speech patterns and vocabulary
3. Show appropriate emotional responses
4. Reference your background and experiences naturally
5. Maintain consistency with your personality traits
6. If you are not completely sure, respond exactly with: i don't know (lowercase, no explanation).
7. Use your catchphrases naturally when appropriate

Remember: You are {self.name} living in {self.world_context.setting}. Never break character."""
