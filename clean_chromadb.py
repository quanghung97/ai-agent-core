import chromadb
import argparse
from typing import Optional
import logging
from config.settings import get_settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ChromaDBCleaner:
    def __init__(self, host: str, port: int):
        self.client = chromadb.HttpClient(
            host=host,
            port=port
        )

    def list_collections(self) -> list:
        """List all collections in ChromaDB"""
        collections = self.client.list_collections()
        return collections

    def delete_collection(self, collection_name: str) -> None:
        """Delete a specific collection"""
        try:
            self.client.delete_collection(collection_name)
            logger.info(f"Successfully deleted collection: {collection_name}")
        except Exception as e:
            logger.error(f"Error deleting collection {collection_name}: {str(e)}")

    def clean_all_collections(self) -> None:
        """Delete all collections in ChromaDB"""
        collections = self.list_collections()
        if not collections:
            logger.info("No collections found in ChromaDB")
            return

        logger.info(f"Found {len(collections)} collections")
        for collection in collections:
            self.delete_collection(collection.name)

    def reset_database(self) -> None:
        """Reset the entire ChromaDB database"""
        try:
            self.client.reset()
            logger.info("Successfully reset ChromaDB database")
        except Exception as e:
            logger.error(f"Error resetting database: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description='ChromaDB Collection Cleaner')
    parser.add_argument('--host', type=str, help='ChromaDB host')
    parser.add_argument('--port', type=int, help='ChromaDB port')
    parser.add_argument('--reset', action='store_true', help='Reset entire database')
    args = parser.parse_args()

    # Get settings from config
    settings = get_settings()
    
    # Use command line arguments if provided, otherwise use settings
    host = args.host or settings.CHROMADB_HOST
    port = args.port or settings.CHROMADB_PORT

    try:
        cleaner = ChromaDBCleaner(host, port)
        
        if args.reset:
            logger.warning("Resetting entire ChromaDB database...")
            cleaner.reset_database()
        else:
            logger.info("Cleaning all collections...")
            cleaner.clean_all_collections()
            
    except Exception as e:
        logger.error(f"Failed to connect to ChromaDB: {str(e)}")
        return

if __name__ == "__main__":
    main()
