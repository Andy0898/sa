from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class LLMConfigurationBase(BaseModel):
    name: str
    model_id: str
    description: Optional[str] = None
    provider: Optional[str] = None
    status: int = 1

class LLMConfigurationResponse(LLMConfigurationBase):
    id: int
    created_time: datetime
    updated_time: Optional[datetime] = None

    class Config:
        from_attributes = True

class ShortcutConfigurationBase(BaseModel):
    name: str
    description: Optional[str] = None
    prompt: str
    model_id: int
    status: int = 1

class ShortcutConfigurationResponse(ShortcutConfigurationBase):
    id: int
    created_time: datetime
    updated_time: Optional[datetime] = None

    class Config:
        from_attributes = True

class ChatRequest(BaseModel):
    prompt: str
    model_id: int

class ChatResponse(BaseModel):
    content: str
    model_name: str 