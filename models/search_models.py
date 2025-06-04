from openai import AsyncOpenAI
from typing import List, Dict, Any
from config.settings import get_settings

settings = get_settings()

class SearchModel:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_MODEL_SEARCH

    async def search(self, query: str) -> Dict[str, Any]:
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                web_search_options={
                    "search_context_size": "low",
                },
                messages=[{
                    "role": "system",
                    "content": "You are a search assistant. Find relevant current information."
                }, {
                    "role": "user",
                    "content": query
                }],
                max_tokens=1000
            )
            return {
                "content": response.choices[0].message.content,
                "search_metadata": response.model_dump()
            }
        except Exception as e:
            raise Exception(f"Search API error: {str(e)}")
