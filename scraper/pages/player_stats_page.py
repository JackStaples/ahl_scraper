from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from typing import List
import time

from config import WAIT_TIME, BASE_URL

class PlayerStatsPage:
    # Locators
    TABLE_LOCATOR = (By.CLASS_NAME, "ht-table")
    PLAYER_ROWS_LOCATOR = (By.CSS_SELECTOR, "tr.ht-odd-row, tr.ht-even-row")
    NEXT_BUTTON_LOCATOR = (By.CSS_SELECTOR, "a[rel='next']")

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
