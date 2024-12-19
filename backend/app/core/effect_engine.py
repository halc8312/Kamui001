from typing import Dict, Any, Optional
import random
import logging
from dataclasses import dataclass

# エフェクトのパラメータを定義するデータクラス
@dataclass
class EffectParameters:
    color: str
    duration: float
    intensity: float
    position: tuple[float, float, float] = (0.0, 0.0, 0.0)

class EffectEngine:
    """
    エフェクト生成エンジン
    様々な視覚・聴覚エフェクトを生成する機能を提供
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._particle_types = ["sparkle", "smoke", "fire", "bubble"]
        self._sound_types = ["explosion", "magic", "ambient", "music"]
        self._light_types = ["point", "spot", "ambient", "directional"]

    def create_particle_effect(
        self, 
        params: EffectParameters,
        particle_type: str = "sparkle"
    ) -> Dict[str, Any]:
        """
        パーティクルエフェクトを生成する

        Args:
            params: エフェクトのパラメータ
            particle_type: パーティクルの種類

        Returns:
            生成されたパーティクルエフェクトの情報
        """
        try:
            if particle_type not in self._particle_types:
                raise ValueError(f"Unsupported particle type: {particle_type}")

            effect = {
                "type": "particle",
                "particle_type": particle_type,
                "color": params.color,
                "duration": params.duration,
                "intensity": params.intensity,
                "position": params.position,
                "particle_count": int(params.intensity * 100),
                "spread_radius": params.intensity * 2.0
            }
            
            self.logger.info(f"Created particle effect: {effect}")
            return effect
            
        except Exception as e:
            self.logger.error(f"Failed to create particle effect: {str(e)}")
            raise

    def create_sound_effect(
        self,
        params: EffectParameters,
        sound_type: str = "magic"
    ) -> Dict[str, Any]:
        """
        サウンドエフェクトを生成する

        Args:
            params: エフェクトのパラメータ
            sound_type: サウンドの種類

        Returns:
            生成されたサウンドエフェクトの情報
        """
        try:
            if sound_type not in self._sound_types:
                raise ValueError(f"Unsupported sound type: {sound_type}")

            effect = {
                "type": "sound",
                "sound_type": sound_type,
                "volume": params.intensity,
                "duration": params.duration,
                "position": params.position,
                "falloff_distance": params.intensity * 10.0,
                "pitch": random.uniform(0.8, 1.2)
            }

            self.logger.info(f"Created sound effect: {effect}")
            return effect

        except Exception as e:
            self.logger.error(f"Failed to create sound effect: {str(e)}")
            raise

    def create_light_effect(
        self,
        params: EffectParameters,
        light_type: str = "point"
    ) -> Dict[str, Any]:
        """
        光エフェクトを生成する

        Args:
            params: エフェクトのパラメータ
            light_type: 光の種類

        Returns:
            生成された光エフェクトの情報
        """
        try:
            if light_type not in self._light_types:
                raise ValueError(f"Unsupported light type: {light_type}")

            effect = {
                "type": "light",
                "light_type": light_type,
                "color": params.color,
                "intensity": params.intensity,
                "duration": params.duration,
                "position": params.position,
                "radius": params.intensity * 5.0,
                "attenuation": 1.0 / (params.intensity + 1.0)
            }

            self.logger.info(f"Created light effect: {effect}")
            return effect

        except Exception as e:
            self.logger.error(f"Failed to create light effect: {str(e)}")
            raise

    def combine_effects(self, *effects: Dict[str, Any]) -> Dict[str, Any]:
        """
        複数のエフェクトを組み合わせる

        Args:
            effects: 組み合わせるエフェクト群

        Returns:
            組み合わされたエフェクト情報
        """
        return {
            "type": "combined",
            "effects": list(effects),
            "total_duration": max(effect["duration"] for effect in effects)
        }