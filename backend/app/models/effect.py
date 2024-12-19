from sqlalchemy import Column, Integer, String, Float, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base
from uuid import uuid4

class Effect(Base):
    """エフェクトモデル
    
    エフェクトの基本情報を管理するモデル
    """
    __tablename__ = "effects"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    name = Column(String(100), nullable=False)
    type = Column(String(50), nullable=False)
    description = Column(String(500))
    created_at = Column(Integer, default=lambda: int(datetime.utcnow().timestamp()))
    updated_at = Column(Integer, default=lambda: int(datetime.utcnow().timestamp()))
    
    # リレーションシップ
    parameters = relationship("EffectParameter", back_populates="effect")
    preset = relationship("EffectPreset", back_populates="effect")

    def to_dict(self):
        """エフェクトの辞書表現を返す"""
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "description": self.description,
            "parameters": [param.to_dict() for param in self.parameters],
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

class EffectPreset(Base):
    """エフェクトプリセットモデル
    
    事前定義されたエフェクト設定を管理するモデル
    """
    __tablename__ = "effect_presets"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    name = Column(String(100), nullable=False)
    effect_id = Column(String(36), ForeignKey("effects.id"))
    settings = Column(JSON)
    created_at = Column(Integer, default=lambda: int(datetime.utcnow().timestamp()))
    
    # リレーションシップ
    effect = relationship("Effect", back_populates="preset")

    def to_dict(self):
        """プリセットの辞書表現を返す"""
        return {
            "id": self.id,
            "name": self.name,
            "effect_id": self.effect_id,
            "settings": self.settings,
            "created_at": self.created_at
        }

class EffectParameter(Base):
    """エフェクトパラメータモデル
    
    エフェクトの各種パラメータを管理するモデル
    """
    __tablename__ = "effect_parameters"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    effect_id = Column(String(36), ForeignKey("effects.id"))
    name = Column(String(50), nullable=False)
    type = Column(String(20), nullable=False)  # number, string, color など
    default_value = Column(String(100))
    min_value = Column(Float)
    max_value = Column(Float)
    unit = Column(String(20))
    
    # リレーションシップ
    effect = relationship("Effect", back_populates="parameters")

    def to_dict(self):
        """パラメータの辞書表現を返す"""
        return {
            "id": self.id,
            "effect_id": self.effect_id,
            "name": self.name,
            "type": self.type,
            "default_value": self.default_value,
            "min_value": self.min_value,
            "max_value": self.max_value,
            "unit": self.unit
        }