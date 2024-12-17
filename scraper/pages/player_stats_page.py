from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from typing import List, Tuple
import time

from config import WAIT_TIME, BASE_URL

class PlayerStatsPage:
    # Locators
    TABLE_LOCATOR = (By.CLASS_NAME, "ht-table")
    PLAYER_ROWS_LOCATOR = (By.CSS_SELECTOR, "tr.ht-odd-row, tr.ht-even-row")
    NEXT_BUTTON_LOCATOR = (By.CSS_SELECTOR, "a[rel='next']")

    SEASON_SELECT_LOCATOR = (By.CSS_SELECTOR, "select[ng-model='selectedSeason']")

    PAGE_URL = BASE_URL + "/stats/player-stats"

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, WAIT_TIME)

    def navigate_to(self):
        """Navigate to the player stats page"""
        self.driver.get(self.PAGE_URL)
        self.wait_for_table()

    def wait_for_table(self):
        """Wait for the stats table to load"""
        self.wait.until(
            EC.presence_of_element_located(self.TABLE_LOCATOR)
        )

    def get_player_rows(self) -> List[WebElement]:
        """Get all player rows from the current page"""
        return self.driver.find_elements(*self.PLAYER_ROWS_LOCATOR)

    def click_next_page(self) -> bool:
        """Click the next page button"""
        try:
            next_button = self.wait.until(
                EC.element_to_be_clickable(self.NEXT_BUTTON_LOCATOR)
            )
            self.driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
            time.sleep(0.5)

            try:
                next_button.click()
                self.wait_for_table()
            except:
                self.driver.execute_script("arguments[0].click();", next_button)

            return True
        except Exception as e:
            print(f"Error clicking next page: {e}")
            return False
    
    def select_season(self, season_id: str) -> bool:
        try:
            select_element = self.wait.until(
                EC.presence_of_element_located(self.SEASON_SELECT_LOCATOR)
            )

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
            select_element = self.wait.until(
                EC.presence_of_element_located(self.SEASON_SELECT_LOCATOR)
            )
            options = select_element.find_elements(By.TAG_NAME, "option")
            return [(option.get_attribute("label"), option.get_attribute("value")) 
                   for option in options]
        except Exception as e:
            print(f"Error getting seasons: {e}")
            return []

    def get_regular_seasons(self) -> List[Tuple[str, str]]:
        all_seasons = self.get_available_seasons()
        # Filter to only include entries with "Regular Season" in the name
        regular_seasons = [(name, id) for name, id in all_seasons if "Regular Season" in name]
        return regular_seasons

