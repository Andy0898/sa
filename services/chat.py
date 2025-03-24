from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain_ollama import OllamaLLM
from typing import Dict, List, Optional
import redis
from core.config import settings

class LLMService:
    def __init__(self):
        self.models = {
            "deepseek-r1": OllamaLLM(model="deepseek-r1"),
            "qwen": OllamaLLM(model="qwen")
        }
        self.redis_client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB
        )
        
    def get_model(self, model_name: str) -> Optional[OllamaLLM]:
        return self.models.get(model_name)
    
    def get_conversation_chain(self, model_name: str, conversation_id: str) -> ConversationChain:
        model = self.get_model(model_name)
        if not model:
            raise ValueError(f"Model {model_name} not found")
        
        # Try to get conversation history from Redis
        memory_key = f"conv:{conversation_id}"
        memory = ConversationBufferMemory()
        
        cached_history = self.redis_client.get(memory_key)
        if cached_history:
            memory.chat_memory.messages = eval(cached_history)
        
        return ConversationChain(
            llm=model,
            memory=memory,
            verbose=True
        )
    
    def save_conversation_history(self, conversation_id: str, history: List[Dict]):
        memory_key = f"conv:{conversation_id}"
        self.redis_client.set(memory_key, str(history), ex=3600)  # Expire after 1 hour
        
    async def generate_response(
        self,
        model_name: str,
        conversation_id: str,
        user_message: str
    ) -> str:
        chain = self.get_conversation_chain(model_name, conversation_id)
        response = await chain.arun(user_message)
        
        # Save updated conversation history
        self.save_conversation_history(
            conversation_id,
            chain.memory.chat_memory.messages
        )
        
        return response 