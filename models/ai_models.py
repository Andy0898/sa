from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, BigInteger
from sqlalchemy.sql import func
from .base import Base

class AiLLMConfiguration(Base):
    """大模型配置表"""
    __tablename__ = "ai_llm_configuration"
    
    llm_id = Column(BigInteger, primary_key=True, autoincrement=True, comment='主键')
    parent_id = Column(BigInteger, default=0, comment='父级 API 主键')
    llm_zh_name = Column(String(100), nullable=False, comment='大模型中文名称')
    llm_en_name = Column(String(100), nullable=False, unique=True, comment='大模型英文简称')
    api_key = Column(String(255), comment='大模型的API Key')
    api_url = Column(String(255), comment='大模型的API URL')
    top_p = Column(Float, default=0, comment='生成过程中的核采样方法概率阈值,取值范围为（0,1.0)')
    temperature = Column(Float, default=0, comment='用于控制模型回复的随机性和多样性,该值介于0到2之间')
    max_tokens = Column(BigInteger, default=1024, comment='模型可生成的最大token个数,一般不超过2000')
    do_sample = Column(Boolean, default=False, comment='启用采样策略,do_sample 为 false 时采样策略 temperature、top_p 将不生效')
    max_chat_limit = Column(BigInteger, default=20, comment='多轮对话次数')
    status = Column(Integer, default=1, comment='LLM状态，1：激活；0：不可用')
    is_local_llm = Column(Boolean, default=False, nullable=False, comment='是否本地大模型。0-本地；1：线上')
    create_by = Column(String(100), comment='创建人')
    create_time = Column(DateTime, server_default=func.current_timestamp(), comment='创建时间')
    update_by = Column(String(100), comment='更新人')
    update_time = Column(DateTime, server_default=func.current_timestamp(), 
                        onupdate=func.current_timestamp(), comment='更新时间')

class AiShortcutConfiguration(Base):
    """快捷助手配置表"""
    __tablename__ = "ai_shotcut_configuration"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, comment='助手名称')
    description = Column(String(200), comment='助手描述')
    prompt = Column(String, nullable=False, comment='提示词')
    model_id = Column(Integer, nullable=False, comment='关联的模型ID')
    status = Column(Integer, default=1, comment='状态：0-禁用，1-启用')
    created_time = Column(DateTime(timezone=True), server_default=func.now())
    updated_time = Column(DateTime(timezone=True), onupdate=func.now()) 