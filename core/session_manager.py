from typing import Dict, Any, Optional
from datetime import datetime
from memory.redis_store import RedisStore
from config.settings import get_settings

settings = get_settings()

class SessionManager:
    def __init__(self):
        self.store = RedisStore()
        self.session_timeout = settings.SESSION_TIMEOUT
    
    async def initialize(self) -> None:
        """Initialize Redis connection"""
        await self.store.initialize()
    
    async def create_session(self, session_id: str, user_id: str) -> Dict[str, Any]:
        session_data = {
            "session_id": session_id,
            "user_id": user_id,
            "created_at": datetime.utcnow().isoformat(),
            "last_active": datetime.utcnow().isoformat(),
            "conversation_history": []
        }
        
        await self.store.set(
            key=f"session:{session_id}",
            value=session_data,
            ttl=self.session_timeout
        )
        return session_data
    
    async def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        return await self.store.get(f"session:{session_id}")
    
    async def update_session(self, session_id: str, data: Dict[str, Any]) -> bool:
        data["last_active"] = datetime.utcnow().isoformat()
        return await self.store.set(
            key=f"session:{session_id}",
            value=data,
            ttl=self.session_timeout
        )
    
    async def delete_session(self, session_id: str) -> bool:
        return await self.store.delete(f"session:{session_id}")
