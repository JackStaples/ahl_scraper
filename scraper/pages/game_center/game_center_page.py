from typing import List
from selenium.webdriver.common.by import By
import time

from scraper.pages.game_center.plays.play_factory import PlayFactory
from scraper.pages.game_center.plays.game_play import GamePlay

from ..base_page import BasePage

class GameCenterPage(BasePage):
    # Locators
    PERIOD_SECTIONS_LOCATOR = (By.CSS_SELECTOR, ".ht-play-by-play > div > div:nth-child(3)")
    EVENT_ROWS_LOCATOR = (By.CSS_SELECTOR, "div.ht-event-row")

    def wait_for_load(self):
        """Wait for the game center page to load"""
        self.wait_for_element_visible(self.PERIOD_SECTIONS_LOCATOR)

    def get_plays(self) -> List[GamePlay]:
        """Get all plays from the game"""
        plays = []

        play_elements = self.driver.find_elements(
            By.CSS_SELECTOR, 
            "div.ht-event-row"
        )

        for element in play_elements:
            play = PlayFactory.create_play(element)
            if play:
                plays.append(play)

        return plays