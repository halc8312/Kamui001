from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
from enum import Enum

class TriggerType(str, Enum):
    """トリガーのタイプを定義するEnum"""
    PRICE = "price"
    VOLUME = "volume"
    TECHNICAL = "technical"
    NEWS = "news"

class TriggerCondition(str, Enum):
    """トリガーの条件を定義するEnum"""
    GREATER_THAN = "greater_than"
    LESS_THAN = "less_than"
    EQUAL_TO = "equal_to"
    CROSSES_ABOVE = "crosses_above"
    CROSSES_BELOW = "crosses_below"

class TriggerBase(BaseModel):
    """トリガーの基本スキーマ"""
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    type: TriggerType
    condition: TriggerCondition
    value: float
    symbol: str = Field(..., min_length=1, max_length=10)
    parameters: Optional[Dict[str, Any]] = Field(default_factory=dict)
    is_active: bool = True

class TriggerCreate(TriggerBase):
    """トリガー作成用スキーマ"""
    pass

class TriggerUpdate(BaseModel):
    """トリガー更新用スキーマ"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    type: Optional[TriggerType] = None
    condition: Optional[TriggerCondition] = None
    value: Optional[float] = None
    symbol: Optional[str] = Field(None, min_length=1, max_length=10)
    parameters: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None

class TriggerResponse(TriggerBase):
    """トリガーレスポンス用スキーマ"""
    id: int
    created_at: datetime
    updated_at: datetime
    user_id: int

    class Config:
        orm_mode = True