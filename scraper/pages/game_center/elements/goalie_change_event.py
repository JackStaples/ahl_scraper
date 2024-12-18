from typing import Optional
from selenium.webdriver.remote.webelement import WebElement

from scraper.pages.game_center.elements.game_event import GameEvent, Player

class GoalieChangeEvent(GameEvent):
    """Represents a goalie change event"""

    def __init__(self, element: WebElement):
        super().__init__(element)
        self.goalie_in = self._get_goalie_in()
        self.goalie_out = self._get_goalie_out()

    def _get_goalie_in(self) -> Optional[Player]:
        """Get the goalie coming in"""
        try:
            section = self.element.find_element(
                By.CSS_SELECTOR, 
                "div.ht-event-details div section"
            )
            return self._parse_player(section)
        except:
            return None

    def _get_goalie_out(self) -> Optional[Player]:
        """Get the goalie going out"""
        try:
            sections = self.element.find_elements(
                By.CSS_SELECTOR, 
                "div.ht-event-details div section"
            )
            if len(sections) > 1:
                return self._parse_player(sections[1])
        except:
            return None
        return None
