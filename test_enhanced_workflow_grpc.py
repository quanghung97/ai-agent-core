import asyncio
import grpc
import uuid
import os
from services.chats import chat_service_pb2, chat_service_pb2_grpc

async def test_single_message():
    async with grpc.aio.insecure_channel('localhost:50051') as channel:
        stub = chat_service_pb2_grpc.ChatServiceStub(channel)
        
        session_id = str(uuid.uuid4())
        
        voice_settings = chat_service_pb2.VoiceSettings(
            stability=0.7,
            similarity_boost=0.7,
            style=0.0,
            use_speaker_boost=True,
            speed=1.0
        )
        
        tts_settings = chat_service_pb2.TTSSettings(
            enable_tts=True,
            voice_id="1l0C0QA9c9jN22EmWiB0",
            voice_settings=voice_settings
        )

        request = chat_service_pb2.ChatRequest(
            user_id="user-001",
            message="Chào bạn, Bạn có thể dự báo thời tiết ngày mai ở Hà Nội không?",
            session_id=session_id,
            context={},
            tts_settings=tts_settings
        )

        response = await stub.ProcessMessage(request)
        
        print("\nReceived response:")
        print(f"Response: {response.response}")
        print(f"Intent: {response.metadata.intent}")
        print(f"Turn count: {response.metadata.turn_count}")
        print(f"Additional data: {response.metadata.additional_data}")

        # Save audio if present
        if response.audio_content:
            os.makedirs('output', exist_ok=True)
            with open(f'output/response_{response.metadata.turn_count}.mp3', 'wb') as f:
                f.write(response.audio_content)
            print(f"Audio saved for response")

async def test_stream_chat():
    async with grpc.aio.insecure_channel('localhost:50051') as channel:
        stub = chat_service_pb2_grpc.ChatServiceStub(channel)
        
        session_id = str(uuid.uuid4())
        user_id = "user-001"

        async def request_generator():
            messages = [
                "Diễn biến tình hình sự kiện Trump đánh thuế lên hàng hóa Trung Quốc 2025",
                "Phản ứng của Trung Quốc là gì?",
                "Ảnh hương của sự kiện này đến nền kinh tế toàn cầu là gì?",
                "Các chyên gia cho rằng đây là một bước đi đúng đắn hay sai lầm?"
            ]
            
            for message in messages:
                yield chat_service_pb2.ChatRequest(
                    user_id=user_id,
                    message=message,
                    session_id=session_id,
                    context={}
                )
                await asyncio.sleep(1)  # Simulate delay between messages

        print("\nStarting streaming chat test...")
        async for response in stub.StreamChat(request_generator()):
            print("\nReceived response:")
            print(f"Response: {response.response}")
            print(f"Intent: {response.metadata.intent}")
            print(f"Turn count: {response.metadata.turn_count}")
            print(f"Additional data: {response.metadata.additional_data}")

async def main():
    print("Testing single message...")
    await test_single_message()
    
    # print("\nTesting streaming chat...")
    # await test_stream_chat()

if __name__ == '__main__':
    asyncio.run(main())
