from pydantic import BaseModel, Field
from typing import Optional, Dict

class EffectBase(BaseModel):
    """エフェクトの基本スキーマ"""
    name: str = Field(..., description="エフェクト名", min_length=1, max_length=100)
    type: str = Field(..., description="エフェクトタイプ")
    parameters: Dict[str, float] = Field(
        ...,
        description="エフェクトのパラメータ",
        example={
            "color": "#FF0000",
            "duration": 1.0,
            "intensity": 0.8
        }
    )

class EffectCreate(EffectBase):
    """エフェクト作成用スキーマ"""
    pass

class EffectUpdate(BaseModel):
    """エフェクト更新用スキーマ"""
    name: Optional[str] = Field(None, description="エフェクト名", min_length=1, max_length=100)
    type: Optional[str] = Field(None, description="エフェクトタイプ")
    parameters: Optional[Dict[str, float]] = Field(
        None,
        description="エフェクトのパラメータ"
    )

class EffectResponse(EffectBase):
    """エフェクトレスポンス用スキーマ"""
    id: str = Field(..., description="エフェクトID")

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "name": "Fade Effect",
                "type": "fade",
                "parameters": {
                    "color": "#FF0000",
                    "duration": 1.0,
                    "intensity": 0.8
                }
            }
        }