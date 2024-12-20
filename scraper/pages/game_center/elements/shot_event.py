from typing import Optional
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By

from scraper.pages.game_center.elements.game_event import GameEvent, Player


class ShotEvent(GameEvent):
    """Represents a shot event"""
    EVENT_SELECTOR = "div.ht-event-details div:nth-child(2)"

    def __init__(self, element: WebElement):
        super().__init__(element, 'Shot')
        self.shooter = self._get_shooter()
        self.goalie = self._get_goalie()

    def _get_shooter(self) -> Optional[Player]:
        """Get the shooting player"""
        try:
            details_div = self.element.find_element(
                By.CSS_SELECTOR, 
                self.EVENT_SELECTOR
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
                self.EVENT_SELECTOR
            )
            # The goalie info comes after the "shoots on" text
            goalie_elements = details_div.find_elements(
                By.CSS_SELECTOR,
                "a[ng-if*='goalie.id']"
            )
            if goalie_elements:
                goalie_section = goalie_elements[0].find_element(By.XPATH, "..")
                return self._parse_goalie(goalie_section)
        except Exception as e:
            print(f"Error getting goalie: {e}")
            return None
        return None

    def _parse_goalie(self, element: WebElement) -> Player:
        """
        Parse goalie information from shot elements.
    
        Args:
            element: WebElement containing goalie information
    
        Returns:
        """
        try:
            spans = element.find_elements(By.TAG_NAME, "span")
            jersey_number = spans[1].text.replace("#", "")
    
            a_tags = element.find_elements(By.TAG_NAME, "a")
            player_link = a_tags[1]
            href = player_link.get_attribute("href")
            player_id = href.split("/")[-2]
    
            name_span = player_link.find_element(By.TAG_NAME, "span")
            name = name_span.text
    
            return Player(
                jersey_number=jersey_number,
                name=name,
                player_id=player_id
            )
        except Exception as e:
            raise ValueError(f"Failed to parse player information: {str(e)}")