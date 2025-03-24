from sqlalchemy.orm import Session
from models.ai_models import AiLLMConfiguration, AiShortcutConfiguration
from models.chat import Conversation, Message
from langchain_ollama import OllamaLLM
from typing import List, Optional, Dict, Any
import logging
from datetime import datetime
import uuid

logger = logging.getLogger(__name__)

class AiService:
    def __init__(self, db: Session):
        self.db = db

    def get_llm_configurations(self, status: Optional[int] = None) -> List[AiLLMConfiguration]:
        """获取大模型配置列表"""
        query = self.db.query(AiLLMConfiguration)
        if status is not None:
            query = query.filter(AiLLMConfiguration.status == status)
        return query.all()

    def get_shortcut_configurations(self, status: Optional[int] = None) -> List[AiShortcutConfiguration]:
        """获取快捷助手配置列表"""
        query = self.db.query(AiShortcutConfiguration)
        if status is not None:
            query = query.filter(AiShortcutConfiguration.status == status)
        return query.all()

    def create_conversation(self, conversation_data: Dict[str, Any], user_id: str, username: str) -> Conversation:
        """创建新的对话"""
        # 验证模型是否存在且可用
        model_id = conversation_data.get("llm_id")
        if not model_id:
            raise ValueError("LLM ID is required")
            
        model = self.db.query(AiLLMConfiguration).filter(
            AiLLMConfiguration.llm_id == model_id,
            AiLLMConfiguration.status == 1
        ).first()
        
        if not model:
            raise ValueError(f"Model with ID {model_id} not found or not active")

        # 生成唯一的会话ID
        conversation_id = str(uuid.uuid4())
        
        conversation = Conversation(
            conversation_id=conversation_id,
            user_id=user_id,
            llm_id=model_id,
            title=conversation_data["title"],
            create_by=username,
            update_by=username
        )
        self.db.add(conversation)
        self.db.commit()
        self.db.refresh(conversation)
        return conversation

    def get_conversation_messages(self, conversation_id: str) -> List[Message]:
        """获取对话的消息历史"""
        # 检查对话是否存在
        conversation = self.db.query(Conversation).filter(
            Conversation.conversation_id == conversation_id
        ).first()
        
        if not conversation:
            raise ValueError(f"Conversation with ID {conversation_id} not found")
            
        # 获取所有相关消息
        messages = self.db.query(Message).filter(
            Message.conversation_id == conversation_id
        ).order_by(Message.create_time).all()
        
        return messages

    async def process_message(self, message_data: Dict[str, Any], username: str) -> Message:
        """处理新消息并获取AI响应"""
        conversation_id = message_data["conversation_id"]
        
        # 检查对话是否存在
        conversation = self.db.query(Conversation).filter(
            Conversation.conversation_id == conversation_id
        ).first()
        
        if not conversation:
            raise ValueError(f"Conversation with ID {conversation_id} not found")

        # 使用对话关联的模型
        model_id = conversation.llm_id

        # 获取模型配置并验证
        model_config = self.db.query(AiLLMConfiguration).filter(
            AiLLMConfiguration.llm_id == model_id,
            AiLLMConfiguration.status == 1
        ).first()
        
        if not model_config:
            raise ValueError(f"Model with ID {model_id} not found or not active")

        try:
            # 生成唯一的消息ID
            message_id = str(uuid.uuid4())
            
            # 准备模型参数
            model_params = {
                "temperature": model_config.temperature,
                "top_p": model_config.top_p,
                "max_tokens": model_config.max_tokens,
                "do_sample": model_config.do_sample
            }

            # 保存用户消息
            message = Message(
                message_id=message_id,
                conversation_id=conversation_id,
                llm_id=model_id,
                question=message_data["content"],
                create_by=username,
                update_by=username
            )
            self.db.add(message)
            self.db.flush()

            # 生成AI回复
            if model_config.is_local_llm:
                # 本地模型使用Ollama
                llm = OllamaLLM(
                    model=model_config.llm_en_name,
                    **model_params
                )
                response = await llm.ainvoke(message_data["content"])
            else:
                # 在线模型处理（需要实现）
                raise NotImplementedError("Online LLM support not implemented yet")

            # 更新消息的回答
            message.answer = response
            
            # 更新对话和消息的时间
            current_time = datetime.utcnow()
            conversation.update_time = current_time
            message.update_time = current_time
            
            self.db.commit()
            self.db.refresh(message)
            return message
            
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            self.db.rollback()
            raise 