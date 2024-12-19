import jwt
import bcrypt
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from fastapi import Request, HTTPException
import logging
from cryptography.fernet import Fernet
import os
from dotenv import load_load_dotenv

# 環境変数の読み込み
load_dotenv()

# ロギングの設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SecurityManager:
    def __init__(self):
        """SecurityManagerの初期化"""
        self.secret_key = os.getenv("SECRET_KEY", "your-secret-key-here")
        self.algorithm = "HS256"
        self.access_token_expire_minutes = 30
        self.fernet_key = Fernet.generate_key()
        self.cipher_suite = Fernet(self.fernet_key)

    async def validate_request(self, request: Request) -> bool:
        """
        リクエストの検証を行う
        
        Args:
            request: FastAPIのRequestオブジェクト
            
        Returns:
            bool: 検証結果
            
        Raises:
            HTTPException: 検証に失敗した場合
        """
        try:
            # Authorization headerの確認
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                raise HTTPException(status_code=401, detail="Invalid authentication credentials")

            # トークンの検証
            token = auth_header.split(" ")[1]
            self.verify_token(token)

            # リクエスト元IPアドレスのログ記録
            client_host = request.client.host
            logger.info(f"Request from IP: {client_host}")

            return True

        except Exception as e:
            logger.error(f"Request validation failed: {str(e)}")
            raise HTTPException(status_code=401, detail="Authentication failed")

    def encrypt_data(self, data: str) -> str:
        """
        データの暗号化を行う
        
        Args:
            data: 暗号化する文字列
            
        Returns:
            str: 暗号化されたデータ
        """
        try:
            encrypted_data = self.cipher_suite.encrypt(data.encode())
            return encrypted_data.decode()
        except Exception as e:
            logger.error(f"Encryption failed: {str(e)}")
            raise Exception("Encryption failed")

    def decrypt_data(self, encrypted_data: str) -> str:
        """
        データの復号化を行う
        
        Args:
            encrypted_data: 暗号化されたデータ
            
        Returns:
            str: 復号化されたデータ
        """
        try:
            decrypted_data = self.cipher_suite.decrypt(encrypted_data.encode())
            return decrypted_data.decode()
        except Exception as e:
            logger.error(f"Decryption failed: {str(e)}")
            raise Exception("Decryption failed")

    def generate_token(self, data: Dict[str, Any]) -> str:
        """
        JWTトークンを生成する
        
        Args:
            data: トークンに含めるデータ
            
        Returns:
            str: 生成されたJWTトークン
        """
        try:
            expiration = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
            to_encode = data.copy()
            to_encode.update({"exp": expiration})
            
            token = jwt.encode(
                to_encode,
                self.secret_key,
                algorithm=self.algorithm
            )
            return token
        except Exception as e:
            logger.error(f"Token generation failed: {str(e)}")
            raise Exception("Token generation failed")

    def verify_token(self, token: str) -> Dict[str, Any]:
        """
        JWTトークンを検証する
        
        Args:
            token: 検証するトークン
            
        Returns:
            Dict[str, Any]: デコードされたトークンのペイロード
            
        Raises:
            HTTPException: トークンが無効な場合
        """
        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm]
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")
        except jwt.JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")

    def hash_password(self, password: str) -> str:
        """
        パスワードをハッシュ化する
        
        Args:
            password: ハッシュ化するパスワード
            
        Returns:
            str: ハッシュ化されたパスワード
        """
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode(), salt).decode()

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        パスワードを検証する
        
        Args:
            plain_password: 平文のパスワード
            hashed_password: ハッシュ化されたパスワード
            
        Returns:
            bool: 検証結果
        """
        return bcrypt.checkpw(
            plain_password.encode(),
            hashed_password.encode()
        )