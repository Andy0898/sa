from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from models.base import get_db
from services.ai_service import AiService
from schemas.ai_models import (
    LLMConfigurationResponse,
    ShortcutConfigurationResponse,
)
from schemas.chat import (
    ConversationCreate,
    ConversationResponse,
    MessageCreate,
    MessageResponse
)

router = APIRouter(prefix="/chat", tags=["chat"])

@router.get("/models", response_model=List[LLMConfigurationResponse])
async def get_available_models(
    status: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """获取可用的大模型列表
    
    Args:
        status: 可选，模型状态（0-禁用，1-启用）
        db: 数据库会话
    """
    service = AiService(db)
    return service.get_llm_configurations(status)

@router.get("/shortcuts", response_model=List[ShortcutConfigurationResponse])
async def get_shortcuts(
    status: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """获取快捷助手列表
    
    Args:
        status: 可选，助手状态（0-禁用，1-启用）
        db: 数据库会话
    """
    service = AiService(db)
    return service.get_shortcut_configurations(status)

@router.post("/conversations", response_model=ConversationResponse)
async def create_conversation(
    conversation: ConversationCreate,
    db: Session = Depends(get_db)
):
    """创建新的对话"""
    service = AiService(db)
    return service.create_conversation(conversation)

@router.post("/conversations/{conversation_id}/messages", response_model=MessageResponse)
async def create_message(
    conversation_id: int,
    request: Dict[str, Any],
    db: Session = Depends(get_db)
):
    """发送消息并获取回复
    
    Args:
        conversation_id: 对话ID
        request: 请求体，包含：
            - content: str 消息内容
            - model_id: int 可选，使用的模型ID
            - params: dict 可选，额外的参数
    """
    try:
        service = AiService(db)
        
        # 验证请求体
        if not isinstance(request, dict):
            raise HTTPException(status_code=400, detail="Invalid request format")
        
        content = request.get("content")
        if not content:
            raise HTTPException(status_code=400, detail="Message content is required")
            
        # 创建消息请求
        message = MessageCreate(
            conversation_id=conversation_id,
            content=content,
            model_id=request.get("model_id"),
            params=request.get("params", {})
        )
        
        # 处理消息
        return await service.process_message(message)
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/conversations/{conversation_id}/messages", response_model=List[MessageResponse])
async def get_conversation_messages(
    conversation_id: int,
    db: Session = Depends(get_db)
):
    """获取对话的消息历史"""
    service = AiService(db)
    return service.get_conversation_messages(conversation_id) 