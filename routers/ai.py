from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from models.base import get_db
from services.ai_service import AiService
from schemas.ai_models import (
    LLMConfigurationResponse,
    ShortcutConfigurationResponse,
    ChatRequest,
    ChatResponse
)

router = APIRouter(prefix="/ai", tags=["ai"])

@router.get("/llm/list", response_model=List[LLMConfigurationResponse])
async def get_llm_list(
    status: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """获取大模型列表
    
    Args:
        status: 可选，模型状态（0-禁用，1-启用）
        db: 数据库会话
    """
    service = AiService(db)
    return service.get_llm_configurations(status)

@router.get("/shortcut/list", response_model=List[ShortcutConfigurationResponse])
async def get_shortcut_list(
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

@router.post("/chat", response_model=ChatResponse)
async def chat_with_llm(
    request: ChatRequest,
    db: Session = Depends(get_db)
):
    """与大模型对话
    
    Args:
        request: 包含prompt和model_id的请求体
        db: 数据库会话
    """
    try:
        service = AiService(db)
        content = await service.chat_with_llm(request.model_id, request.prompt)
        
        # 获取模型名称
        model = db.query(AiLLMConfiguration).filter(
            AiLLMConfiguration.id == request.model_id
        ).first()
        
        return ChatResponse(
            content=content,
            model_name=model.name if model else "Unknown"
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 