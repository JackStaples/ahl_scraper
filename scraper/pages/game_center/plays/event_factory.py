from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from typing import Optional

from scraper.pages.game_center.plays.event_types import EventType

from .game_play import GameEvent

class EventFactory:
    """Factory class for creating game events"""

    @staticmethod
    def create_event(element: WebElement) -> Optional[GameEvent]:
        """Create the appropriate event object based on the event type

        Args:
            element (WebElement): The event row element

        Returns:
            Optional[GameEvent]: The appropriate event object or None if not supported
        """
        try:
            event_name = element.find_element(By.CSS_SELECTOR, "div.ht-event-type").text
            event_type = EventType.from_text(event_name)
            
            if event_type:
                return event_type.create_event(element)

            print(f"Unsupported event type: {event_name}")
            return None
        except Exception as e:
            print(f"Error creating event: {e}")
            return None
