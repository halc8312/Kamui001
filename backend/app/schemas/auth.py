from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ApiKeyCreate(BaseModel):
    """APIキー作成のためのスキーマ"""
    name: str = Field(..., min_length=1, max_length=100, description="APIキーの名前")
    expires_at: Optional[datetime] = Field(None, description="APIキーの有効期限")
    permissions: list[str] = Field(default=["read"], description="APIキーの権限リスト")

    class Config:
        schema_extra = {
            "example": {
                "name": "Production API Key",
                "expires_at": "2024-12-31T23:59:59",
                "permissions": ["read", "write"]
            }
        }

class TokenValidation(BaseModel):
    """トークン検証のためのスキーマ"""
    token: str = Field(..., description="検証するトークン")
    token_type: str = Field(default="bearer", description="トークンタイプ")

    class Config:
        schema_extra = {
            "example": {
                "token": "eyJhbGciOiJIUzI1NiIs...",
                "token_type": "bearer"
            }
        }

class AuthResponse(BaseModel):
    """認証レスポンスのためのスキーマ"""
    access_token: str = Field(..., description="アクセストークン")
    token_type: str = Field(default="bearer", description="トークンタイプ")
    expires_in: int = Field(..., description="トークンの有効期限（秒）")
    user_id: str = Field(..., description="認証されたユーザーのID")
    permissions: list[str] = Field(default=["read"], description="ユーザーの権限リスト")

    class Config:
        schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIs...",
                "token_type": "bearer",
                "expires_in": 3600,
                "user_id": "user_123",
                "permissions": ["read", "write"]
            }
        }

    @property
    def token_header(self) -> str:
        """
        認証ヘッダーの文字列を生成
        Returns:
            str: 'Bearer {token}' 形式の文字列
        """
        return f"{self.token_type.title()} {self.access_token}"