from fastapi import APIRouter
from typing import Dict, Any, Optional
from pydantic import BaseModel
import logging
from pathlib import Path
import json
import yaml

# 内部モジュールのインポート
from app.core.minecraft_bridge import MinecraftConnection
from app.core.effect_engine import EffectEngine

# ロガーの設定
logger = logging.getLogger(__name__)

# APIルーターの初期化
router = APIRouter()

class EffectConfig(BaseModel):
    """エフェクト設定を管理するクラス"""
    name: str
    type: str
    parameters: Dict[str, Any]
    duration: Optional[int] = None
    intensity: Optional[float] = None
    
    class Config:
        arbitrary_types_allowed = True

def load_presets() -> Dict[str, EffectConfig]:
    """
    プリセットエフェクトを設定ファイルから読み込む
    
    Returns:
        Dict[str, EffectConfig]: プリセットエフェクトの辞書
    """
    try:
        preset_path = Path(__file__).parent / "presets.yaml"
        with open(preset_path) as f:
            presets_data = yaml.safe_load(f)
        
        return {
            name: EffectConfig(**config)
            for name, config in presets_data.items()
        }
    except Exception as e:
        logger.error(f"プリセット読み込みエラー: {e}")
        return {}

def validate_effect_params(effect_config: EffectConfig) -> bool:
    """
    エフェクトパラメータの検証
    
    Args:
        effect_config: 検証するエフェクト設定
        
    Returns:
        bool: 検証結果
    """
    try:
        # 基本的なパラメータの存在チェック
        required_params = {"type", "parameters"}
        if not all(hasattr(effect_config, param) for param in required_params):
            return False
            
        # タイプ別の追加検証
        if effect_config.type == "particle":
            if "color" not in effect_config.parameters:
                return False
        elif effect_config.type == "sound":
            if "volume" not in effect_config.parameters:
                return False
                
        return True
    except Exception as e:
        logger.error(f"パラメータ検証エラー: {e}")
        return False

async def initialize_effects(effect_engine: EffectEngine) -> None:
    """
    エフェクトシステムの初期化
    
    Args:
        effect_engine: エフェクトエンジンインスタンス
    """
    try:
        # プリセットの読み込み
        presets = load_presets()
        
        # エフェクトエンジンの初期化
        await effect_engine.initialize()
        
        # プリセットの登録
        for preset_name, preset_config in presets.items():
            if validate_effect_params(preset_config):
                await effect_engine.register_effect(preset_name, preset_config)
                
    except Exception as e:
        logger.error(f"エフェクト初期化エラー: {e}")
        raise

async def setup_minecraft_connection() -> MinecraftConnection:
    """
    Minecraft接続の設定
    
    Returns:
        MinecraftConnection: 設定済みのMinecraft接続インスタンス
    """
    try:
        connection = MinecraftConnection()
        await connection.connect()
        
        # 接続設定
        connection.set_timeout(30)
        connection.enable_auto_reconnect()
        
        return connection
    except Exception as e:
        logger.error(f"Minecraft接続エラー: {e}")
        raise

# エフェクトエンジンのグローバルインスタンス
effect_engine: Optional[EffectEngine] = None
minecraft_connection: Optional[MinecraftConnection] = None

# 初期化時に実行
async def startup():
    """アプリケーション起動時の初期化"""
    global effect_engine, minecraft_connection
    
    minecraft_connection = await setup_minecraft_connection()
    effect_engine = EffectEngine(minecraft_connection)
    await initialize_effects(effect_engine)

# シャットダウン時に実行
async def shutdown():
    """アプリケーション終了時のクリーンアップ"""
    if minecraft_connection:
        await minecraft_connection.disconnect()