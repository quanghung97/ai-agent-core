import chromadb
from typing import List, Dict, Any, Optional
from config.settings import get_settings
import tiktoken
import uuid
from openai import AsyncOpenAI

settings = get_settings()

class KnowledgeMemory:
    def __init__(self, collection_name, max_tokens: int = 500, overlap_tokens: int = 50):
        self.client = None
        self.collection_name = collection_name
        self.collection = None
        self.max_tokens = max_tokens
        self.overlap_tokens = overlap_tokens
        self.tokenizer = tiktoken.get_encoding("cl100k_base")
        self.openai_client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    def _validate_metadata(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and convert metadata to acceptable format for ChromaDB"""
        valid_metadata = {}
        for key, value in metadata.items():
            if isinstance(value, (str, int, float, bool)) or value is None:
                valid_metadata[key] = value
            elif isinstance(value, list):
                valid_metadata[key] = ','.join(str(x) for x in value)
            else:
                valid_metadata[key] = str(value)
        return valid_metadata

    def _chunk_text(self, text: str) -> List[Dict[str, Any]]:
        """Split text into overlapping chunks based on token count with smart splitting"""
        tokens = self.tokenizer.encode(text)
        chunks = []
        
        i = 0
        while i < len(tokens):
            # Get chunk tokens
            chunk_end = min(i + self.max_tokens, len(tokens))
            chunk_tokens = tokens[i:chunk_end]
            
            # Find better break point if possible
            if chunk_end < len(tokens) and len(chunk_tokens) > self.overlap_tokens:
                # Look for sentence endings within the last portion of the chunk
                break_chars = {'.', '?', '!', '\n'}
                search_range = range(len(chunk_tokens)-self.overlap_tokens, len(chunk_tokens))
                
                for j in reversed(search_range):
                    if self.tokenizer.decode([chunk_tokens[j]]).strip() in break_chars:
                        chunk_tokens = chunk_tokens[:j + 1]
                        break
            
            # Decode chunk tokens back to text and clean it
            chunk_text = self.tokenizer.decode(chunk_tokens).strip()
            
            if chunk_text:  # Only add non-empty chunks
                chunk_info = {
                    "text": chunk_text,
                    "token_count": len(chunk_tokens),
                    "start_pos": i,
                    "end_pos": i + len(chunk_tokens)
                }
                chunks.append(chunk_info)
            
            # Move forward, accounting for overlap
            i += max(1, len(chunk_tokens) - self.overlap_tokens)
            
        return chunks

    async def initialize(self):
        """Initialize or get the collection"""
        try:
            if not self.client:
                self.client = chromadb.HttpClient(
                    host=settings.CHROMADB_HOST,
                    port=settings.CHROMADB_PORT,
                )

                print("ChromaDB client initialized")
            self.collection = self.client.get_or_create_collection(
                name=self.collection_name
            )
        except Exception as e:
            raise Exception(f"Failed to initialize collection: {str(e)}")

    async def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings using OpenAI API"""
        try:
            response = await self.openai_client.embeddings.create(
                model="text-embedding-3-small",
                input=texts
            )
            return [item.embedding for item in response.data]
        except Exception as e:
            raise Exception(f"Failed to generate embeddings: {str(e)}")

    async def load_knowledge_base(self, knowledge_data: List[Dict[str, Any]]):
        """Load knowledge from JSON data into ChromaDB with text chunking"""
        try:
            if not self.collection:
                await self.initialize()

            documents = []
            metadatas = []
            ids = []
            
            for entry in knowledge_data:
                # Split text into chunks with metadata
                text_chunks = self._chunk_text(entry["text"])
                
                # Create document entries for each chunk
                for chunk_idx, chunk_info in enumerate(text_chunks):
                    chunk_id = f"{entry['id']}_chunk_{chunk_idx}"
                    documents.append(chunk_info["text"])
                    
                    # Validate and update metadata
                    chunk_metadata = self._validate_metadata(entry["metadata"].copy())
                    chunk_metadata.update({
                        "chunk_index": chunk_idx,
                        "total_chunks": len(text_chunks),
                        "original_id": entry["id"],
                        "token_count": chunk_info["token_count"],
                        "start_pos": chunk_info["start_pos"],
                        "end_pos": chunk_info["end_pos"]
                    })
                    metadatas.append(chunk_metadata)
                    ids.append(chunk_id)

            # Add to ChromaDB if there are documents
            print(f"Adding {len(documents)} chunks to collection '{self.collection_name}'")
            if documents:
                print(f"Generating embeddings for {len(documents)} chunks...")
                embeddings = await self.generate_embeddings(documents)
                print(f"Adding documents with embeddings to collection '{self.collection_name}'")
                self.collection.add(
                    embeddings=embeddings,
                    documents=documents,
                    metadatas=metadatas,
                    ids=ids
                )
        except Exception as e:
            print("Failed to add to collection:", e)

    async def query_knowledge(self, query: str, n_results: int = 3) -> List[Dict[str, Any]]:
        """Query the knowledge base using semantic search"""
        if not self.collection:
            await self.initialize()

        # Generate embedding for query
        query_embedding = await self.generate_embeddings([query])

        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=n_results,
            include=["documents", "metadatas", "distances"]
        )

        # Format and merge results
        formatted_results = []
        seen_original_ids = set()
        
        for i in range(len(results["documents"][0])):
            original_id = results["metadatas"][0][i]["original_id"]
            
            if original_id not in seen_original_ids:
                seen_original_ids.add(original_id)
                formatted_results.append({
                    "content": results["documents"][0][i],
                    "metadata": {
                        k: v for k, v in results["metadatas"][0][i].items() 
                        if k not in ["chunk_index", "total_chunks", "original_id"]
                    },
                    "relevance_score": 1 - results["distances"][0][i]
                })

        return formatted_results
