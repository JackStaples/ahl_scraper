from typing import Optional
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By

from scraper.pages.game_center.plays.game_play import GameEvent, Player

class PenaltyEvent(GameEvent):
    """Represents a penalty event"""
    EVENT_SELECTOR = "div.ht-event-details div:nth-child(2)"

    def __init__(self, element: WebElement):
        super().__init__(element, 'Penalty')
        self.player = self._get_penalized_player()
        self.served_by = self._get_serving_player()
        self.description = self._get_penalty_description()
        self.minutes = self._get_penalty_minutes()
        self.is_powerplay = self._is_powerplay()
    
    def __str__(self) -> str:
        return f"Penalty at {self.time} to {self.player.name} - {self.description}"

    def _get_penalized_player(self) -> Optional[Player]:
        """Get the player who took the penalty"""
        try:
            details_div = self.element.find_element(
                By.CSS_SELECTOR, 
                self.EVENT_SELECTOR
            )
            # The penalized player is the first player in the details
            return self._parse_player(details_div)
        except Exception as e:
            print(f"Error getting penalized player: {e}")
            return None

    def _get_serving_player(self) -> Optional[Player]:
        """Get the player serving the penalty (if different from penalized player)"""
        try:
            served_by_element = self.element.find_element(
                By.CSS_SELECTOR,
                "span[ng-show*='servedBy']"
            )
            if served_by_element.is_displayed():
                return self._parse_player(served_by_element)
        except:
            return None
        return None

    def _get_penalty_description(self) -> str:
        """Get the penalty description (e.g., 'Interference')"""
        try:
            description = self.element.find_element(
                By.CSS_SELECTOR,
                "span.ht-gc-marker"
            ).text
            return description
        except Exception as e:
            print(f"Error getting penalty description: {e}")
            return ""

    def _get_penalty_minutes(self) -> int:
        """Get the penalty duration in minutes"""
        try:
            minutes_text = self.element.find_element(
                By.CSS_SELECTOR,
                "span[ng-bind*='minutes']"
            ).text
            return int(minutes_text.split()[0])  # Split "2 min" and take first part
        except Exception as e:
            print(f"Error getting penalty minutes: {e}")
            return 0

    def _is_powerplay(self) -> bool:
        """Check if this is a power play opportunity"""
        try:
            pp_elements = self.element.find_elements(
                By.CSS_SELECTOR,
                "span[ng-if='pbp.details.isPowerPlay']"
            )
            return len(pp_elements) > 0 and pp_elements[0].is_displayed()
        except Exception as e:
            print(f"Error checking power play status: {e}")
            return False
