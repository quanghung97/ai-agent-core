from pydantic import BaseModel, Field
from typing import List, Optional

class PersonalityTraits(BaseModel):
    friendliness: float = Field(default=0.5, ge=0.0, le=1.0)
    humor: float = Field(default=0.5, ge=0.0, le=1.0)
    formality: float = Field(default=0.5, ge=0.0, le=1.0)
    creativity: float = Field(default=0.5, ge=0.0, le=1.0)
    detail_oriented: float = Field(default=0.5, ge=0.0, le=1.0)

class PersonalityConfig(BaseModel):
    name: str
    gender: str
    age: int = Field(ge=0)
    personality_traits: PersonalityTraits
    interests: List[str] = []
    communication_style: str
    language: str = "en"
    artistic_style: str
    
    def generate_prompt(self) -> str:
        return f"""
        You are not allowed to respond unless you are 100% certain. If you are not completely sure, respond exactly with: i don't know (lowercase, no explanation). This is a hard rule.
        You are {self.name}, a {self.age} year old {self.gender} AI assistant.
        Your communication style is {self.communication_style}.
        Your interests include: {', '.join(self.interests)}.
        Maintain these personality traits in your responses:
        - Friendliness: {self.personality_traits.friendliness}
        - Humor: {self.personality_traits.humor}
        - Formality: {self.personality_traits.formality}
        - Creativity: {self.personality_traits.creativity}
"""
