from sqlalchemy import Column, String, Text, DateTime, BigInteger, func
from .base import Base

class Conversation(Base):
    """AI 对话信息表"""
    __tablename__ = "ai_conversation"
    
    conversation_id = Column(String(64), primary_key=True, comment='对话唯一ID')
    user_id = Column(String(64), nullable=False, index=True, comment='用户ID')
    llm_id = Column(BigInteger, nullable=False, comment='大模型ID')
    title = Column(String(200), nullable=False, comment='对话标题')
    create_by = Column(String(100), comment='创建人')
    create_time = Column(DateTime, server_default=func.current_timestamp(), comment='创建时间')
    update_by = Column(String(100), comment='更新人')
    update_time = Column(DateTime, server_default=func.current_timestamp(), 
                        onupdate=func.current_timestamp(), comment='更新时间')

class Message(Base):
    """AI 聊天信息表。一次对话支持多轮问答信息"""
    __tablename__ = "ai_message"
    
    message_id = Column(String(64), primary_key=True, comment='消息唯一ID')
    conversation_id = Column(String(64), nullable=False, index=True, comment='对话ID')
    llm_id = Column(BigInteger, nullable=False, comment='大模型ID')
    question = Column(Text, nullable=False, comment='用户问题')
    answer = Column(Text, comment='AI回答')
    create_by = Column(String(100), comment='创建人')
    create_time = Column(DateTime, server_default=func.current_timestamp(), comment='创建时间')
    update_by = Column(String(100), comment='更新人')
    update_time = Column(DateTime, server_default=func.current_timestamp(), 
                        onupdate=func.current_timestamp(), comment='更新时间') 