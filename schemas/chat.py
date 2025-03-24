from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime

class ConversationBase(BaseModel):
    title: str
    model_id: Optional[int] = None
    params: Dict[str, Any] = Field(default_factory=dict)

class ConversationCreate(ConversationBase):
    pass

class ConversationResponse(ConversationBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class MessageBase(BaseModel):
    content: str
    role: str = "user"
    model_id: Optional[int] = None
    params: Dict[str, Any] = Field(default_factory=dict)

class MessageCreate(MessageBase):
    conversation_id: int

class MessageResponse(MessageBase):
    id: int
    conversation_id: int
    created_at: datetime
    model_name: Optional[str] = None
    response: Optional[Dict[str, Any]] = None  # 存储模型返回的完整响应

    class Config:
        from_attributes = True

# 用于API响应的通用格式
class ApiResponse(BaseModel):
    success: bool = True
    data: Optional[Any] = None
    error: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict) 