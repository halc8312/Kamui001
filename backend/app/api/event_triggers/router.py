from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.services import trigger_service
from app.schemas.trigger import (
    TriggerCreate,
    TriggerUpdate,
    Trigger,
    Message
)
from app.core.auth import get_current_user

router = APIRouter(
    prefix="/triggers",
    tags=["triggers"]
)

class TriggerController:
    def __init__(self, trigger_service=trigger_service):
        self.trigger_service = trigger_service

    async def create_trigger(self, trigger_data: TriggerCreate, user_id: str) -> Trigger:
        """
        新しいトリガーを作成する
        
        Args:
            trigger_data: 作成するトリガーのデータ
            user_id: トリガーを作成するユーザーのID
            
        Returns:
            作成されたトリガーオブジェクト
        """
        try:
            return await self.trigger_service.create_trigger(trigger_data, user_id)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    async def list_triggers(self, user_id: str) -> List[Trigger]:
        """
        ユーザーのトリガー一覧を取得する
        
        Args:
            user_id: トリガーを取得するユーザーのID
            
        Returns:
            トリガーオブジェクトのリスト
        """
        try:
            return await self.trigger_service.get_triggers_by_user(user_id)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    async def update_trigger(self, trigger_id: str, trigger_data: TriggerUpdate, user_id: str) -> Trigger:
        """
        既存のトリガーを更新する
        
        Args:
            trigger_id: 更新するトリガーのID
            trigger_data: 更新するトリガーのデータ
            user_id: トリガーを更新するユーザーのID
            
        Returns:
            更新されたトリガーオブジェクト
        """
        try:
            return await self.trigger_service.update_trigger(trigger_id, trigger_data, user_id)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    async def delete_trigger(self, trigger_id: str, user_id: str) -> Message:
        """
        トリガーを削除する
        
        Args:
            trigger_id: 削除するトリガーのID
            user_id: トリガーを削除するユーザーのID
            
        Returns:
            削除完了メッセージ
        """
        try:
            return await self.trigger_service.delete_trigger(trigger_id, user_id)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

trigger_controller = TriggerController()

@router.post("/create", response_model=Trigger)
async def create_trigger(
    trigger_data: TriggerCreate,
    current_user = Depends(get_current_user)
):
    return await trigger_controller.create_trigger(trigger_data, current_user.id)

@router.get("/list", response_model=List[Trigger])
async def list_triggers(
    current_user = Depends(get_current_user)
):
    return await trigger_controller.list_triggers(current_user.id)

@router.put("/{trigger_id}", response_model=Trigger)
async def update_trigger(
    trigger_id: str,
    trigger_data: TriggerUpdate,
    current_user = Depends(get_current_user)
):
    return await trigger_controller.update_trigger(trigger_id, trigger_data, current_user.id)

@router.delete("/{trigger_id}", response_model=Message)
async def delete_trigger(
    trigger_id: str,
    current_user = Depends(get_current_user)
):
    return await trigger_controller.delete_trigger(trigger_id, current_user.id)