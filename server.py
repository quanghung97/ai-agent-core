import asyncio
import grpc
import sys
import signal
from concurrent import futures
from services.chat_service_impl import ChatServiceImpl
from services.chats.chat_service_pb2_grpc import add_ChatServiceServicer_to_server
from services.chats.chat_service_pb2 import DESCRIPTOR
from grpc_reflection.v1alpha import reflection
import logging
from config.settings import get_settings
from services.vector_store.vector_store_service_pb2_grpc import add_VectorStoreServiceServicer_to_server
from services.vector_store_service_impl import VectorStoreServiceImpl

logger = logging.getLogger(__name__)
settings = get_settings()

class GrpcServer:
    def __init__(self, host: str = "localhost", port: int = 50051, max_workers: int = 10):
        self.host = host
        self.port = port
        self.max_workers = max_workers
        self.server = None
        self._shutdown_event = asyncio.Event()

    async def start(self):
        """Start the gRPC server"""
        self.server = grpc.aio.server(
            futures.ThreadPoolExecutor(max_workers=self.max_workers),
            options=[
                ('grpc.max_send_message_length', 100 * 1024 * 1024),
                ('grpc.max_receive_message_length', 100 * 1024 * 1024)
            ]
        )
        
        # Add Chat Service
        service = ChatServiceImpl()
        add_ChatServiceServicer_to_server(service, self.server)
        
        # Add Vector Store Service
        vector_store_service = VectorStoreServiceImpl()
        add_VectorStoreServiceServicer_to_server(vector_store_service, self.server)
        
        # Enable reflection
        SERVICE_NAMES = (
            DESCRIPTOR.services_by_name['ChatService'].full_name,
            reflection.SERVICE_NAME,
        )
        reflection.enable_server_reflection(SERVICE_NAMES, self.server)
        
        # Start server
        server_address = f'{self.host}:{self.port}'
        self.server.add_insecure_port(server_address)
        await self.server.start()
        logger.info(f"Server started on {server_address}")
        logger.info(f"App Name: {settings.APP_NAME}")
        logger.info(f"Debug Mode: {settings.DEBUG}")
        
        try:
            await self._shutdown_event.wait()
        finally:
            await self.shutdown()

    async def shutdown(self):
        """Gracefully shutdown the server"""
        if self.server:
            logger.info("Shutting down server...")
            await self.server.stop(5)  # 5 seconds grace period
            logger.info("Server shutdown complete")

    def signal_handler(self, sig):
        """Handle shutdown signals"""
        logger.info(f"Received signal {sig}")
        asyncio.create_task(self.initiate_shutdown())

    async def initiate_shutdown(self):
        """Initiate the shutdown process"""
        self._shutdown_event.set()

async def main():
    """Main entry point"""
    if not (3, 11) <= sys.version_info < (3, 14):
        sys.exit("This project requires Python 3.11–3.13.")

    logging.basicConfig(
        level=logging.DEBUG if settings.DEBUG else logging.INFO
    )
    
    # Create server with settings
    server = GrpcServer(
        host=getattr(settings, 'GRPC_HOST', 'localhost'),
        port=getattr(settings, 'GRPC_PORT', 50051)
    )
    
    # Setup signal handlers for Windows
    signal.signal(signal.SIGINT, server.signal_handler)
    signal.signal(signal.SIGTERM, server.signal_handler)
    
    try:
        await server.start()
    except Exception as e:
        logger.error(f"Server error: {e}")
        raise
    finally:
        logger.info("Cleanup complete")

if __name__ == "__main__":
    asyncio.run(main())
