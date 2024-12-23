from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from typing import Optional

from scraper.pages.game_center.plays.play_types import PlayType

from .game_play import GamePlay

class PlayFactory:
    """Factory class for creating game plays"""

    @staticmethod
    def create_play(element: WebElement) -> Optional[GamePlay]:
        """Create the appropriate play object based on the play type

        Args:
            element (WebElement): The play row element

        Returns:
            Optional[GamePlay]: The appropriate play object or None if not supported
        """
        try:
            play_name = element.find_element(By.CSS_SELECTOR, "div.ht-event-type").text
            play_type = PlayType.from_text(play_name)
            
            if play_type:
                return play_type.create_play(element)

            print(f"Unsupported play type: {play_name}")
            return None
        except Exception as e:
            print(f"Error creating play: {e}")
            return None
