# AI Chat API

A FastAPI backend for an AI chat application with support for multiple LLM models and conversation history.

## Features

- Multiple LLM model support (deepseek-r1, qwen)
- Conversation history management
- Redis-based caching for chat history
- MySQL database for structured data
- Authentication and authorization
- RESTful API endpoints

## Prerequisites

- Python 3.8+
- MySQL 8.0+
- Redis
- Ollama (for LLM models)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd ai-chat-api
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file with the following variables:
```env
SECRET_KEY=your-secret-key
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your-password
MYSQL_DB=chat_db
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
```

5. Initialize the database:
```bash
python init_db.py
```

## Running the Application

Start the FastAPI server:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, you can access:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### Chat
- `POST /api/v1/chat/conversations` - Create a new conversation
- `GET /api/v1/chat/conversations` - List user's conversations
- `POST /api/v1/chat/conversations/{conversation_id}/messages` - Send a message
- `GET /api/v1/chat/conversations/{conversation_id}/messages` - Get conversation messages

## Project Structure

```
.
├── main.py
├── requirements.txt
├── README.md
├── core/
│   └── config.py
├── models/
│   ├── base.py
│   └── chat.py
├── routers/
│   └── chat.py
├── schemas/
│   └── chat.py
├── services/
│   └── chat.py
└── dependencies/
    └── auth.py
``` 
## 项目架构
1. 采用分层架构：
   - routers/ (API端点)
   - models/ (Pydantic和SQLAlchemy模型)
   - schemas/ (数据验证模型)
   - services/ (业务逻辑)
   - utils/ (工具函数)
   - dependencies/ (依赖注入)
   - core/ (配置和安全)