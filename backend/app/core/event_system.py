from typing import Dict, List, Callable, Any
from dataclasses import dataclass
from datetime import datetime
import logging
import asyncio
from concurrent.futures import ThreadPoolExecutor

logger = logging.getLogger(__name__)

@dataclass
class Event:
    """イベントデータを表現するクラス"""
    type: str
    payload: Dict[str, Any]
    timestamp: datetime = datetime.now()

class EventSystem:
    """
    イベント管理システム
    イベントの登録、処理、エフェクトの発動を管理する
    """
    
    def __init__(self):
        self._handlers: Dict[str, List[Callable]] = {}
        self._executor = ThreadPoolExecutor(max_workers=4)
        self._active = True

    def register_handler(self, event_type: str, handler: Callable) -> None:
        """
        イベントハンドラーを登録する

        Args:
            event_type (str): イベントタイプ
            handler (Callable): ハンドラー関数
        """
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(handler)
        logger.info(f"Registered handler for event type: {event_type}")

    async def process_event(self, event: Event) -> None:
        """
        イベントを処理する

        Args:
            event (Event): 処理するイベント
        """
        if not self._active:
            logger.warning("Event system is not active")
            return

        if event.type not in self._handlers:
            logger.warning(f"No handlers registered for event type: {event.type}")
            return

        try:
            handlers = self._handlers[event.type]
            tasks = []
            
            for handler in handlers:
                # 非同期ハンドラーの場合は直接実行
                if asyncio.iscoroutinefunction(handler):
                    tasks.append(asyncio.create_task(handler(event)))
                else:
                    # 同期ハンドラーの場合はThreadPoolExecutorで実行
                    tasks.append(
                        asyncio.get_event_loop().run_in_executor(
                            self._executor,
                            handler,
                            event
                        )
                    )
            
            await asyncio.gather(*tasks)
            logger.info(f"Successfully processed event: {event.type}")
            
        except Exception as e:
            logger.error(f"Error processing event {event.type}: {str(e)}")
            raise

    async def trigger_effect(self, effect_type: str, parameters: Dict[str, Any]) -> None:
        """
        エフェクトを発動する

        Args:
            effect_type (str): エフェクトタイプ
            parameters (Dict[str, Any]): エフェクトのパラメータ
        """
        effect_event = Event(
            type=f"effect_{effect_type}",
            payload={
                "type": effect_type,
                "parameters": parameters
            }
        )
        
        try:
            await self.process_event(effect_event)
            logger.info(f"Effect triggered: {effect_type}")
        except Exception as e:
            logger.error(f"Error triggering effect {effect_type}: {str(e)}")
            raise

    def shutdown(self) -> None:
        """イベントシステムをシャットダウンする"""
        self._active = False
        self._executor.shutdown(wait=True)
        logger.info("Event system shutdown completed")

# シングルトンインスタンスの作成
event_system = EventSystem()
