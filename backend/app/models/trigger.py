from enum import Enum
from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field

class ConditionOperator(str, Enum):
    """条件演算子の定義"""
    EQUALS = "equals"
    GREATER_THAN = "greater_than"
    LESS_THAN = "less_than"
    CONTAINS = "contains"
    BETWEEN = "between"

class ActionType(str, Enum):
    """アクションタイプの定義"""
    NOTIFICATION = "notification"
    EMAIL = "email"
    WEBHOOK = "webhook"
    API_CALL = "api_call"

class EventCondition(BaseModel):
    """イベント条件モデル"""
    field: str = Field(..., description="条件を適用するフィールド名")
    operator: ConditionOperator = Field(..., description="条件演算子")
    value: Any = Field(..., description="比較値")
    additional_params: Optional[Dict[str, Any]] = Field(default=None, description="追加パラメータ")

    class Config:
        schema_extra = {
            "example": {
                "field": "price",
                "operator": "greater_than",
                "value": 100.0,
                "additional_params": {"tolerance": 0.01}
            }
        }

class TriggerAction(BaseModel):
    """トリガーアクションモデル"""
    action_type: ActionType = Field(..., description="アクションのタイプ")
    parameters: Dict[str, Any] = Field(..., description="アクションのパラメータ")
    priority: int = Field(default=1, ge=1, le=5, description="アクションの優先度")
    retry_count: int = Field(default=3, ge=0, description="リトライ回数")

    class Config:
        schema_extra = {
            "example": {
                "action_type": "notification",
                "parameters": {
                    "message": "Price alert triggered",
                    "channel": "email"
                },
                "priority": 2,
                "retry_count": 3
            }
        }

class Trigger(BaseModel):
    """トリガーモデル"""
    id: Optional[str] = Field(default=None, description="トリガーID")
    name: str = Field(..., description="トリガー名")
    description: Optional[str] = Field(default=None, description="トリガーの説明")
    conditions: List[EventCondition] = Field(..., description="トリガー条件のリスト")
    actions: List[TriggerAction] = Field(..., description="実行するアクションのリスト")
    is_active: bool = Field(default=True, description="トリガーの有効/無効状態")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="作成日時")
    updated_at: Optional[datetime] = Field(default=None, description="更新日時")
    
    class Config:
        schema_extra = {
            "example": {
                "name": "Price Alert Trigger",
                "description": "Triggers when stock price exceeds threshold",
                "conditions": [{
                    "field": "price",
                    "operator": "greater_than",
                    "value": 100.0
                }],
                "actions": [{
                    "action_type": "notification",
                    "parameters": {
                        "message": "Price alert triggered",
                        "channel": "email"
                    },
                    "priority": 1
                }],
                "is_active": True
            }
        }