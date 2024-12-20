from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from typing import Optional

from scraper.pages.game_center.elements.goal_event import GoalEvent

from .game_event import GameEvent
from .goalie_change_event import GoalieChangeEvent
from .shot_event import ShotEvent
from .penalty_event import PenaltyEvent

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
            event_type = element.find_element(By.CSS_SELECTOR, "div.ht-event-type").text

            if "GOALIE CHANGE" in event_type:
                return GoalieChangeEvent(element)
            elif "SHOT" in event_type:
                return ShotEvent(element)
            elif "PENALTY" in event_type:
                return PenaltyEvent(element)
            elif "GOAL" in event_type:
                return GoalEvent(element)
            
            print(f"Unsupported event type: {event_type}")
            return None
        except Exception as e:
            print(f"Error creating event: {e}")
            return None
