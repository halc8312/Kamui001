import asyncio
import websockets
import json
import logging
from typing import Optional, Dict, Any, Callable
from contextlib import asynccontextmanager

# ロギングの設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MinecraftConnection:
    """Minecraftサーバーとの接続を管理するクラス"""
    
    def __init__(self, host: str = "localhost", port: int = 25565):
        self.host = host
        self.port = port
        self.websocket: Optional[websockets.WebSocketServerProtocol] = None
        self.event_handlers: Dict[str, Callable] = {}
        self.is_connected = False

    async def connect(self) -> bool:
        """
        Minecraftサーバーへの接続を確立
        
        Returns:
            bool: 接続成功の場合True
        """
        try:
            uri = f"ws://{self.host}:{self.port}"
            self.websocket = await websockets.connect(uri)
            self.is_connected = True
            logger.info(f"Successfully connected to Minecraft server at {uri}")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to Minecraft server: {str(e)}")
            return False

    async def disconnect(self):
        """サーバーとの接続を切断"""
        if self.websocket:
            await self.websocket.close()
            self.is_connected = False
            logger.info("Disconnected from Minecraft server")

    async def send_effect(self, effect_data: Dict[str, Any]) -> bool:
        """
        エフェクトをMinecraftサーバーに送信
        
        Args:
            effect_data: エフェクトのパラメータを含む辞書
            
        Returns:
            bool: 送信成功の場合True
        """
        if not self.is_connected or not self.websocket:
            logger.error("Not connected to Minecraft server")
            return False

        try:
            message = json.dumps({
                "type": "effect",
                "data": effect_data
            })
            await self.websocket.send(message)
            logger.info(f"Sent effect: {effect_data}")
            return True
        except Exception as e:
            logger.error(f"Failed to send effect: {str(e)}")
            return False

    async def listen_events(self):
        """
        Minecraftサーバーからのイベントをリッスン
        """
        if not self.is_connected or not self.websocket:
            logger.error("Not connected to Minecraft server")
            return

        try:
            async for message in self.websocket:
                try:
                    data = json.loads(message)
                    event_type = data.get("type")
                    
                    if event_type in self.event_handlers:
                        await self.event_handlers[event_type](data.get("data"))
                    else:
                        logger.warning(f"Unhandled event type: {event_type}")
                        
                except json.JSONDecodeError:
                    logger.error("Received invalid JSON message")
                    
        except websockets.exceptions.ConnectionClosed:
            logger.warning("Connection to Minecraft server closed")
            self.is_connected = False

    def register_event_handler(self, event_type: str, handler: Callable):
        """
        イベントハンドラーを登録
        
        Args:
            event_type: イベントの種類
            handler: イベントを処理するコールバック関数
        """
        self.event_handlers[event_type] = handler

    @asynccontextmanager
    async def connection(self):
        """
        コンテキストマネージャーとしての接続管理
        """
        try:
            await self.connect()
            yield self
        finally:
            await self.disconnect()

# 使用例
async def example_usage():
    minecraft = MinecraftConnection()
    
    async def handle_player_join(data):
        logger.info(f"Player joined: {data}")
    
    minecraft.register_event_handler("player_join", handle_player_join)
    
    async with minecraft.connection():
        # エフェクトの送信例
        effect = {
            "name": "particle_effect",
            "parameters": {
                "type": "explosion",
                "x": 100,
                "y": 64,
                "z": 100
            }
        }
        await minecraft.send_effect(effect)
        
        # イベントリスニングの開始
        await minecraft.listen_events()

if __name__ == "__main__":
    asyncio.run(example_usage())