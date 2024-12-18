from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from typing import List, Tuple
import time

from .base_page import BasePage
from config import BASE_URL

class PlayerStatsPage(BasePage):
    # Locators
    TABLE_LOCATOR = (By.CLASS_NAME, "ht-table")
    PLAYER_ROWS_LOCATOR = (By.CSS_SELECTOR, "tr.ht-odd-row, tr.ht-even-row")
    NEXT_BUTTON_LOCATOR = (By.CSS_SELECTOR, "a[rel='next']")
    SEASON_SELECT_LOCATOR = (By.CSS_SELECTOR, "select[ng-model='selectedSeason']")

    PAGE_URL = BASE_URL + "/stats/player-stats"

    def navigate_to(self):
        """Navigate to the player stats page"""
        self.driver.get(self.PAGE_URL)
        self.wait_for_table()

    def wait_for_table(self):
        """Wait for the stats table to load"""
        self.find_element(self.TABLE_LOCATOR)

    def get_player_rows(self) -> List[WebElement]:
        """Get all player rows from the current page"""
        return self.find_elements(self.PLAYER_ROWS_LOCATOR)

    def click_next_page(self) -> bool:
        """Click the next page button"""
        try:
            next_button = self.find_element(self.NEXT_BUTTON_LOCATOR)
            self.scroll_to_element(next_button)
            time.sleep(0.5)
            return self.click_element(self.NEXT_BUTTON_LOCATOR)
        except Exception as e:
            print(f"Error clicking next page: {e}")
            return False

    def select_season(self, season_id: str) -> bool:
        try:
            select_element = self.find_element(self.SEASON_SELECT_LOCATOR)

            self.driver.execute_script(
                """
                var select = arguments[0];
                select.value = arguments[1];
                angular.element(select).triggerHandler('change');
                """, 
                select_element, 
                season_id
            )

            time.sleep(1)
            self.wait_for_table()
            return True

        except Exception as e:
            print(f"Error selecting season: {e}")
            return False

    def get_available_seasons(self) -> List[Tuple[str, str]]:
        """
        Get all available seasons and their IDs
        Returns:
            List of tuples containing (season_name, season_id)
        """
        try:
            select_element = self.find_element(self.SEASON_SELECT_LOCATOR)
            options = select_element.find_elements(By.TAG_NAME, "option")
            return [(option.get_attribute("label"), option.get_attribute("value")) 
                   for option in options]
        except Exception as e:
            print(f"Error getting seasons: {e}")
            return []

    def get_regular_seasons(self) -> List[Tuple[str, str]]:
        all_seasons = self.get_available_seasons()
        return [(name, id) for name, id in all_seasons if "Regular Season" in name]
