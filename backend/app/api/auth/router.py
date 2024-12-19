from fastapi import APIRouter, Depends, HTTPException
from typing import Optional

from app.services.auth_service import AuthService
from app.schemas.auth import (
    UserCreate,
    ApiKey,
    ValidationResult,
    Message
)
from app.core.security import get_current_user

router = APIRouter(prefix="/auth", tags=["authentication"])

class AuthController:
    def __init__(self):
        self.auth_service = AuthService()

    async def generate_api_key(self, user_data: UserCreate) -> ApiKey:
        """
        新しいAPIキーを生成する
        
        Args:
            user_data (UserCreate): ユーザー作成データ
            
        Returns:
            ApiKey: 生成されたAPIキー情報
        """
        try:
            return await self.auth_service.create_api_key(user_data)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    async def validate_token(self, token: str) -> ValidationResult:
        """
        トークンの有効性を検証する
        
        Args:
            token (str): 検証対象のトークン
            
        Returns:
            ValidationResult: トークン検証結果
        """
        try:
            return await self.auth_service.validate_token(token)
        except Exception as e:
            raise HTTPException(status_code=401, detail="Invalid token")

    async def revoke_token(self, token: str) -> Message:
        """
        トークンを無効化する
        
        Args:
            token (str): 無効化対象のトークン
            
        Returns:
            Message: 処理結果メッセージ
        """
        try:
            return await self.auth_service.revoke_token(token)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

auth_controller = AuthController()

@router.post("/api-key")
async def generate_api_key(
    user_data: UserCreate,
    current_user: Optional[dict] = Depends(get_current_user)
) -> ApiKey:
    """APIキー生成エンドポイント"""
    return await auth_controller.generate_api_key(user_data)

@router.post("/validate")
async def validate_token(token: str) -> ValidationResult:
    """トークン検証エンドポイント"""
    return await auth_controller.validate_token(token)

@router.delete("/revoke")
async def revoke_token(
    token: str,
    current_user: Optional[dict] = Depends(get_current_user)
) -> Message:
    """トークン無効化エンドポイント"""
    return await auth_controller.revoke_token(token)