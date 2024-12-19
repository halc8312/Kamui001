from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.services import effect_service
from app.schemas.effect import (
    Effect,
    EffectCreate,
    EffectUpdate,
    EffectPreset,
    TriggerData,
    EffectResult,
    Message
)
from app.core.minecraft_bridge import MinecraftBridge
from app.core.dependencies import get_minecraft_bridge

router = APIRouter(prefix="/effects", tags=["effects"])

class EffectController:
    def __init__(self, minecraft_bridge: MinecraftBridge):
        self.minecraft_bridge = minecraft_bridge
        self.effect_service = effect_service.EffectService(minecraft_bridge)

@router.post("/create", response_model=Effect)
async def create_effect(
    effect_data: EffectCreate,
    controller: EffectController = Depends(lambda bridge=Depends(get_minecraft_bridge): EffectController(bridge))
) -> Effect:
    """
    新しい魔法エフェクトを作成します
    
    Args:
        effect_data: 作成するエフェクトのデータ
        
    Returns:
        作成されたエフェクト情報
    """
    try:
        return await controller.effect_service.create_effect(effect_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/presets", response_model=List[EffectPreset])
async def get_presets(
    controller: EffectController = Depends(lambda bridge=Depends(get_minecraft_bridge): EffectController(bridge))
) -> List[EffectPreset]:
    """
    利用可能なエフェクトプリセットのリストを取得します
    
    Returns:
        エフェクトプリセットのリスト
    """
    return await controller.effect_service.get_presets()

@router.post("/trigger", response_model=EffectResult)
async def trigger_effect(
    effect_id: str,
    trigger_data: TriggerData,
    controller: EffectController = Depends(lambda bridge=Depends(get_minecraft_bridge): EffectController(bridge))
) -> EffectResult:
    """
    指定されたエフェクトを実行します
    
    Args:
        effect_id: 実行するエフェクトのID
        trigger_data: トリガー実行に必要なデータ
        
    Returns:
        エフェクト実行結果
    """
    try:
        return await controller.effect_service.trigger_effect(effect_id, trigger_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{effect_id}", response_model=Effect)
async def update_effect(
    effect_id: str,
    effect_data: EffectUpdate,
    controller: EffectController = Depends(lambda bridge=Depends(get_minecraft_bridge): EffectController(bridge))
) -> Effect:
    """
    既存のエフェクトを更新します
    
    Args:
        effect_id: 更新するエフェクトのID
        effect_data: 更新するエフェクトデータ
        
    Returns:
        更新されたエフェクト情報
    """
    try:
        return await controller.effect_service.update_effect(effect_id, effect_data)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{effect_id}", response_model=Message)
async def delete_effect(
    effect_id: str,
    controller: EffectController = Depends(lambda bridge=Depends(get_minecraft_bridge): EffectController(bridge))
) -> Message:
    """
    指定されたエフェクトを削除します
    
    Args:
        effect_id: 削除するエフェクトのID
        
    Returns:
        削除結果のメッセージ
    """
    try:
        return await controller.effect_service.delete_effect(effect_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))