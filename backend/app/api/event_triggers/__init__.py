"""
Event Triggers API Initialization Module
This module handles the initialization and configuration of event triggers system.
"""

from fastapi import APIRouter
from typing import Dict, List, Optional
from pydantic import BaseModel

from app.core.event_system import EventSystem
from app.services.trigger_service import TriggerService

# Initialize router
router = APIRouter()

class TriggerConfig(BaseModel):
    """Configuration class for managing trigger settings"""
    name: str
    event_type: str
    conditions: Dict
    actions: List[Dict]
    enabled: bool = True
    priority: int = 0
    description: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "name": "price_alert",
                "event_type": "price_change",
                "conditions": {"threshold": 5.0},
                "actions": [{"type": "notification", "params": {}}],
                "enabled": True,
                "priority": 1,
                "description": "Price change alert trigger"
            }
        }

def register_event_types() -> None:
    """
    Register all supported event types in the system
    """
    event_types = [
        "price_change",
        "volume_spike",
        "technical_indicator",
        "market_status",
        "news_alert"
    ]
    
    for event_type in event_types:
        EventSystem.register_event_type(event_type)

def setup_listeners() -> None:
    """
    Configure and set up event listeners for different trigger types
    """
    trigger_service = TriggerService()
    
    # Setup core event listeners
    EventSystem.add_listener("price_change", trigger_service.handle_price_trigger)
    EventSystem.add_listener("volume_spike", trigger_service.handle_volume_trigger)
    EventSystem.add_listener("technical_indicator", trigger_service.handle_technical_trigger)
    EventSystem.add_listener("market_status", trigger_service.handle_market_status_trigger)
    EventSystem.add_listener("news_alert", trigger_service.handle_news_trigger)

async def initialize_triggers() -> None:
    """
    Initialize the trigger system and perform necessary setup
    This function should be called during application startup
    """
    try:
        # Register supported event types
        register_event_types()
        
        # Setup event listeners
        setup_listeners()
        
        # Load saved trigger configurations
        await TriggerService.load_trigger_configurations()
        
        # Initialize monitoring systems
        await TriggerService.initialize_monitoring()
        
    except Exception as e:
        # Log the error and raise it for proper handling
        logger.error(f"Failed to initialize trigger system: {str(e)}")
        raise

# Export necessary components
__all__ = [
    "router",
    "TriggerConfig",
    "register_event_types",
    "setup_listeners",
    "initialize_triggers"
]