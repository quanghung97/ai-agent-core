# AI Agent Core Project

🤖 **Hệ thống AI Agent đa tính năng với LangGraph, OpenAI, và ElevenLabs**

Một core service mạnh mẽ để xây dựng AI agents có khả năng chat, tạo ảnh, xử lý giọng nói và cá nhân hóa tính cách. Hỗ trợ scale lên đến 100,000 người dùng với 1,000 active sessions đồng thời.

## ✨ Tính năng chính

### 🗣️ **Đa phương thức giao tiếp**
- **Chat AI**: Tích hợp ChatOpenAI (GPT-3.5, GPT-4o, GPT-4o-mini)
- **Tạo ảnh**: DALL-E 2/3 cho image generation và editing
- **Nhận diện giọng nói**: OpenAI Whisper STT
- **Chuyển đổi văn bản thành giọng**: ElevenLabs TTS

### 🧠 **Trí nhớ thông minh**
- **Short-term Memory**: Lưu trữ lịch sử trò chuyện trong session
- **Long-term Memory**: Học hỏi và nhớ preferences, personality của user
- **Persistent Storage**: Redis backend cho performance cao

### 👤 **Cá nhân hóa AI Agent**
- Cấu hình tính cách, sở thích, giới tính
- Role-playing với nhiều nhân vật khác nhau
- Template library cho các character phổ biến
- Dynamic personality switching

### 🚀 **Hiệu suất cao**
- Hỗ trợ 10 người dùng/agent đồng thời
- Scale lên đến 1,000 active sessions
- Kafka integration cho communication với backend
- Redis clustering cho memory management

### 🔧 **Đa mô hình AI**
- Support multiple OpenAI model versions
- Dynamic model switching based on requirements
- Cost optimization với model selection
- Fallback mechanisms

## 📁 Cấu trúc Project

```
ai-agent-core/
├── 📄 README.md
├── 📄 requirements.txt
├── 🐳 docker-compose.yml
├── 🐳 Dockerfile
├── 🔧 .env.example
├── 📄 .gitignore
│
├── ⚙️ config/                          # Cấu hình hệ thống
│   ├── __init__.py
│   ├── settings.py                     # Cấu hình chung
│   ├── kafka_config.py                 # Cấu hình Kafka messaging
│   ├── openai_config.py                # Cấu hình OpenAI models
│   ├── elevenlabs_config.py            # Cấu hình ElevenLabs TTS
│   └── logging_config.py               # Cấu hình logging system
│
├── 🧠 core/                            # Core system components
│   ├── __init__.py
│   ├── agent_manager.py                # Quản lý lifecycle AI agents
│   ├── session_manager.py              # Quản lý user sessions & concurrency
│   ├── memory_manager.py               # Quản lý short/long-term memory
│   ├── model_registry.py               # Registry các AI models
│   └── exceptions.py                   # Custom exception classes
│
├── 🤖 agents/                          # AI Agent implementations
│   ├── __init__.py
│   ├── base_agent.py                   # Base class cho tất cả agents
│   ├── personality_agent.py            # Agent với personality system
│   ├── chat_agent.py                   # Xử lý chat conversations
│   ├── image_agent.py                  # DALL-E image generation/editing
│   ├── voice_agent.py                  # STT/TTS voice processing
│   └── multi_modal_agent.py            # Multi-modal workflow agent
│
├── 🕸️ graphs/                          # LangGraph workflow definitions
│   ├── __init__.py
│   ├── base_graph.py                   # Base LangGraph configuration
│   ├── chat_graph.py                   # Chat workflow graph
│   ├── image_graph.py                  # Image processing workflow
│   ├── voice_graph.py                  # Voice processing workflow
│   └── multi_modal_graph.py            # Multi-modal workflow graph
│
├── 🔮 models/                          # AI Model wrappers
│   ├── __init__.py
│   ├── openai_models.py                # ChatGPT model integrations
│   ├── dalle_models.py                 # DALL-E 2/3 model wrappers
│   ├── whisper_models.py               # Whisper STT model wrapper
│   └── elevenlabs_models.py            # ElevenLabs TTS integration
│
├── 🛠️ services/                        # Business logic services
│   ├── __init__.py
│   ├── chat_service.py                 # Chat processing & management
│   ├── image_service.py                # Image generation & editing
│   ├── stt_service.py                  # Speech-to-text processing
│   ├── tts_service.py                  # Text-to-speech processing
│   ├── personality_service.py          # Personality configuration
│   └── memory_service.py               # Memory management service
│
├── 🧠 memory/                          # Memory management system
│   ├── __init__.py
│   ├── short_term_memory.py            # Session-based memory
│   ├── long_term_memory.py             # Persistent user memory
│   ├── memory_store.py                 # Memory storage interface
│   └── redis_store.py                  # Redis implementation
│
├── 📨 messaging/                       # Kafka messaging system
│   ├── __init__.py
│   ├── kafka_producer.py               # Gửi messages đến NestJS
│   ├── kafka_consumer.py               # Nhận messages từ NestJS
│   ├── message_handler.py              # Xử lý message routing
│   └── message_types.py                # Message type definitions
│
├── 👤 personality/                     # AI Personality system
│   ├── __init__.py
│   ├── personality_config.py           # Personality data models
│   ├── role_playing.py                 # Role-playing logic
│   ├── character_templates.py          # Pre-defined characters
│   └── personality_loader.py           # Load/save personality configs
│
├── 🔧 utils/                           # Utility functions
│   ├── __init__.py
│   ├── audio_utils.py                  # Audio processing utilities
│   ├── image_utils.py                  # Image processing utilities
│   ├── text_utils.py                   # Text processing utilities
│   ├── validation.py                   # Input validation helpers
│   └── rate_limiter.py                 # Rate limiting utilities
│
├── 📊 monitoring/                      # System monitoring
│   ├── __init__.py
│   ├── metrics.py                      # Performance metrics collection
│   ├── health_check.py                 # Health check endpoints
│   └── logger.py                       # Structured logging
│
├── 🧪 tests/                           # Test suites
│   ├── __init__.py
│   ├── conftest.py                     # Pytest configuration
│   ├── unit/                           # Unit tests
│   │   ├── test_agents.py              # Agent functionality tests
│   │   ├── test_services.py            # Service layer tests
│   │   ├── test_memory.py              # Memory system tests
│   │   └── test_messaging.py           # Kafka messaging tests
│   ├── integration/                    # Integration tests
│   │   ├── test_workflows.py           # End-to-end workflow tests
│   │   ├── test_kafka_integration.py   # Kafka integration tests
│   │   └── test_openai_integration.py  # OpenAI API integration tests
│   └── performance/                    # Performance tests
│       ├── test_concurrent_users.py    # Concurrent user load tests
│       └── test_load.py                # System load testing
│
├── 📜 scripts/                         # Utility scripts
│   ├── setup_kafka.sh                  # Kafka setup automation
│   ├── run_agents.py                   # Agent startup script
│   ├── migrate_memory.py               # Memory migration utilities
│   └── performance_test.py             # Performance testing script
│
└── 🚀 main.py                          # Application entry point
```

### 📋 Component Responsibilities

| Component | Chức năng chính | Scaling Strategy |
|-----------|----------------|------------------|
| **🧠 Core** | Agent lifecycle, session management, memory coordination | Horizontal + Redis clustering |
| **🤖 Agents** | AI processing, personality handling, multi-modal workflows | Load balancing per agent type |
| **🕸️ Graphs** | LangGraph workflow orchestration, state management | Stateless processing |
| **🔮 Models** | AI model integration, version management, fallback handling | Model caching + connection pooling |
| **🛠️ Services** | Business logic, data processing, API abstraction | Service-specific scaling |
| **🧠 Memory** | Short/long-term storage, user context, conversation history | Redis clustering + partitioning |
| **📨 Messaging** | Kafka communication, async processing, event handling | Kafka partitioning + consumer groups |
| **👤 Personality** | Character configuration, role-playing, behavior modeling | Template caching |
| **📊 Monitoring** | Metrics collection, health checks, performance tracking | Centralized monitoring |

### 🔄 Data Flow Architecture

```
┌─────────────────┐
│   User Request  │
│   (via NestJS)  │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐    ┌─────────────────┐
│ Kafka Consumer  │◄──►│ Message Handler │
│   (messaging)   │    │   (messaging)   │
└─────────┬───────┘    └─────────────────┘
          │
          ▼
┌─────────────────┐    ┌─────────────────┐
│ Session Manager │◄──►│ Memory Manager  │
│     (core)      │    │     (memory)    │
└─────────┬───────┘    └─────────────────┘
          │
          ▼
┌─────────────────┐    ┌─────────────────┐
│ Agent Manager   │◄──►│ Personality     │
│     (core)      │    │   (personality) │
└─────────┬───────┘    └─────────────────┘
          │
          ▼
┌─────────────────┐    ┌─────────────────┐
│ LangGraph       │◄──►│ AI Models       │
│   (graphs)      │    │   (models)      │
└─────────┬───────┘    └─────────────────┘
          │
          ▼
┌─────────────────┐    ┌─────────────────┐
│ Response        │◄──►│ Kafka Producer  │
│ Processing      │    │   (messaging)   │
└─────────────────┘    └─────────────────┘
```

## 🛠️ Cài đặt

### Prerequisites

- Python 3.9+
- Docker & Docker Compose
- Redis Server
- Apache Kafka

### Quick Start

1. **Clone repository**
```bash
git clone https://github.com/your-org/ai-agent-core.git
cd ai-agent-core
```

2. **Setup environment**
```bash
cp .env.example .env
# Chỉnh sửa các API keys trong .env file
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Start services với Docker**
```bash
docker-compose up -d
```

5. **Run AI Agent Core**
```bash
python main.py
```

6. **Generate Services Proto**
```bash
cd d:\ai-agent\ai-agent-core
python -m grpc_tools.protoc -I../ai-agent-proto --python_out=. --grpc_python_out=. --pyi_out=. ../ai-agent-proto/services/chats/chat_service.proto
```

## ⚙️ Cấu hình

### Environment Variables

```bash
# OpenAI Configuration
OPENAI_API_KEY=sk-your-openai-api-key
OPENAI_ORG_ID=org-your-organization-id
OPENAI_DEFAULT_MODEL=gpt-4o-mini

# ElevenLabs Configuration
ELEVENLABS_API_KEY=your-elevenlabs-api-key
ELEVENLABS_DEFAULT_VOICE=rachel

# Kafka Configuration
KAFKA_BOOTSTRAP_SERVERS=localhost:9092
KAFKA_TOPIC_PREFIX=ai_agent
KAFKA_GROUP_ID=ai_agent_core

# Redis Configuration
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=your-redis-password

# Application Configuration
MAX_CONCURRENT_USERS=1000
MAX_USERS_PER_AGENT=10
SESSION_TIMEOUT=3600
LOG_LEVEL=INFO

# Performance Tuning
WORKER_PROCESSES=4
MEMORY_CACHE_SIZE=1000
MODEL_CACHE_TTL=3600
```

### Personality Configuration

```python
# Ví dụ cấu hình personality
personality_config = {
    "name": "Luna",
    "gender": "female",
    "age": 25,
    "personality_traits": {
        "friendliness": 0.9,
        "humor": 0.7,
        "formality": 0.3,
        "creativity": 0.8
    },
    "interests": ["technology", "music", "travel"],
    "communication_style": "casual_friendly",
    "voice_settings": {
        "provider": "elevenlabs",
        "voice_id": "rachel",
        "speed": 1.0,
        "pitch": 0.0
    }
}
```

## 🚀 Sử dụng

### Basic Chat Agent

```python
from agents.chat_agent import ChatAgent
from personality.personality_config import PersonalityConfig

# Khởi tạo agent với personality
personality = PersonalityConfig.load_from_file("personalities/luna.json")
agent = ChatAgent(personality=personality)

# Bắt đầu conversation
response = await agent.chat(
    user_id="user123",
    message="Xin chào! Bạn có khỏe không?",
    session_id="session456"
)

print(response.content)  # AI response
```

### Image Generation

```python
from agents.image_agent import ImageAgent

agent = ImageAgent()

# Tạo ảnh từ text
image_url = await agent.generate_image(
    prompt="A beautiful sunset over mountains",
    size="1024x1024",
    model="dall-e-3"
)

# Chỉnh sửa ảnh có sẵn
edited_image = await agent.edit_image(
    image_url="https://example.com/image.jpg",
    prompt="Add a rainbow in the sky",
    mask_url="https://example.com/mask.jpg"
)
```

### Voice Processing

```python
from agents.voice_agent import VoiceAgent

agent = VoiceAgent()

# Speech to Text
text = await agent.speech_to_text(
    audio_file="recording.wav",
    language="vi"
)

# Text to Speech
audio_url = await agent.text_to_speech(
    text="Xin chào, tôi là Luna!",
    voice="rachel",
    language="vi"
)
```

### Multi-Modal Workflow

```python
from agents.multi_modal_agent import MultiModalAgent

agent = MultiModalAgent(personality=personality)

# Xử lý input phức tạp
response = await agent.process_multi_modal(
    user_id="user123",
    text_input="Tạo cho tôi một bức ảnh về",
    image_input="https://example.com/reference.jpg",
    audio_input="description.wav",
    session_id="session456"
)
```

## 📊 Monitoring & Performance

### Metrics Dashboard

Hệ thống tích hợp Prometheus metrics:

- **Response Time**: Thời gian xử lý request
- **Concurrent Users**: Số người dùng đang active
- **Memory Usage**: Sử dụng memory và cache
- **Model Performance**: Hiệu suất của từng AI model
- **Error Rates**: Tỷ lệ lỗi theo từng component

### Health Checks

```bash
# Kiểm tra health của services
curl http://localhost:8000/health

# Chi tiết status của các components
curl http://localhost:8000/health/detailed
```

### Performance Testing

```bash
# Chạy load test
python scripts/performance_test.py --concurrent-users 100 --duration 300

# Test memory performance
python scripts/test_memory_performance.py --operations 10000
```

## 🧪 Testing

```bash
# Unit tests
pytest tests/unit/ -v

# Integration tests
pytest tests/integration/ -v

# Performance tests
pytest tests/performance/ -v

# Coverage report
pytest --cov=. --cov-report=html
```

## 🐳 Docker Deployment

### Production Docker Compose

```yaml
version: '3.8'
services:
  ai-agent-core:
    image: ai-agent-core:latest
    environment:
      - REDIS_HOST=redis-cluster
      - KAFKA_BOOTSTRAP_SERVERS=kafka-cluster:9092
    deploy:
      replicas: 3
      resources:
        limits:
          memory: 4G
          cpus: '2'
    
  redis-cluster:
    image: redis:7-alpine
    deploy:
      replicas: 3
    
  kafka-cluster:
    image: confluentinc/cp-kafka:latest
    deploy:
      replicas: 3
```

### Kubernetes Deployment

```bash
# Deploy to Kubernetes
kubectl apply -f k8s/

# Scale agents
kubectl scale deployment ai-agent-core --replicas=5

# Monitor pods
kubectl get pods -l app=ai-agent-core
```

## 🔒 Security

### API Security
- JWT token validation với NestJS backend
- Rate limiting per user/IP
- Input sanitization và validation
- Encrypted communication với Redis/Kafka

### Data Privacy
- PII data encryption at rest
- Secure memory cleanup
- GDPR compliance cho user data
- Audit logging cho sensitive operations

## 📈 Scaling Guide

### Horizontal Scaling

1. **Agent Instances**: Scale based on concurrent users
   ```bash
   # Tăng số instances
   docker-compose up --scale ai-agent-core=5
   ```

2. **Redis Clustering**: Setup Redis cluster cho memory consistency
   ```bash
   # Redis cluster setup
   ./scripts/setup_redis_cluster.sh
   ```

3. **Kafka Partitioning**: Partition messages theo user groups
   ```bash
   # Tăng Kafka partitions
   kafka-topics --alter --topic ai_agent_chat --partitions 10
   ```

### Vertical Scaling

- **Memory**: 4GB+ RAM per instance cho model caching
- **CPU**: 2+ cores per instance cho concurrent processing
- **GPU**: Optional cho local model inference

### Load Balancing

```nginx
upstream ai_agents {
    least_conn;
    server ai-agent-1:8000 weight=3;
    server ai-agent-2:8000 weight=3;
    server ai-agent-3:8000 weight=2;
}
```

## 🤝 Contributing

1. Fork repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

### Development Setup

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Setup pre-commit hooks
pre-commit install

# Run linting
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
black . --check
```

## 📝 License

MIT License - xem file [LICENSE](LICENSE) để biết thêm chi tiết.

## 📞 Support

- **Documentation**: [Wiki](https://github.com/your-org/ai-agent-core/wiki)
- **Issues**: [GitHub Issues](https://github.com/your-org/ai-agent-core/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-org/ai-agent-core/discussions)
- **Email**: support@your-company.com

## 🎯 Roadmap

### Version 2.0
- [ ] Support cho GPT-5 khi release
- [ ] Multi-language personality configs
- [ ] Advanced emotion detection
- [ ] Voice cloning integration

### Version 2.1
- [ ] Custom model fine-tuning
- [ ] Advanced memory compression
- [ ] Real-time collaboration features
- [ ] Mobile SDK integration

---

**Made with ❤️ by [Your Company]**

⭐ **Star this repo if you find it helpful!**
