from typing import Optional
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By

from scraper.pages.game_center.elements.game_event import GameEvent, Player


class ShotEvent(GameEvent):
    """Represents a shot event"""

    def __init__(self, element: WebElement):
        super().__init__(element)
        self.shooter = self._get_shooter()
        self.goalie = self._get_goalie()

    def _get_shooter(self) -> Optional[Player]:
        """Get the shooting player"""
        try:
            details_div = self.element.find_element(
                By.CSS_SELECTOR, 
                "div.ht-event-details div"
            )
            # The shooter is the first player in the details
            return self._parse_player(details_div)
        except Exception as e:
            print(f"Error getting shooter: {e}")
            return None

    def _get_goalie(self) -> Optional[Player]:
        """Get the goalie being shot on"""
        try:
            details_div = self.element.find_element(
                By.CSS_SELECTOR, 
                "div.ht-event-details div"
            )
            # The goalie info comes after the "shoots on" text
            goalie_elements = details_div.find_elements(
                By.CSS_SELECTOR,
                "a[ng-if*='goalie.id']"
            )
            if goalie_elements:
                goalie_section = goalie_elements[0].find_element(By.XPATH, "..")
                return self._parse_player(goalie_section)
        except Exception as e:
            print(f"Error getting goalie: {e}")
            return None
        return None
