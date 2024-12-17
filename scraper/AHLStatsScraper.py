from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from typing import List, Dict
import time

from config import *
from scraper.WebDriverManager import WebDriverManager
from scraper.PlayerParser import PlayerParser

class AHLStatsScraper:
    def __init__(self, headless: bool = True):
        self.driver =  WebDriverManager.create_driver(headless)
        self.parser = PlayerParser()

    def __del__(self):
        try:
            if self.driver is not None:
                self.driver.quit()
                self.driver = None
        except Exception as e:
            print(f"Error closing driver: {e}")

    def close(self):
        """Explicitly close the browser and clean up resources"""
        try:
            if self.driver is not None:
                self.driver.quit()
                self.driver = None
        except Exception as e:
            print(f"Error closing driver: {e}")

    def get_players(self, num_players: int = 100) -> List[Dict]:
        """Get specified number of top players"""
        self.driver.get(BASE_URL)
        self.wait_for_table()

        players = []
        pages_needed = num_players // PLAYERS_PER_PAGE
        current_page = 1

        while current_page <= pages_needed:
            print(f"Scraping page {current_page}...")

            rows = self.driver.find_elements(By.CSS_SELECTOR, "tr.ht-odd-row, tr.ht-even-row")
            for row in rows:
                player_data = self.parser.parse_player_row(row)
                if player_data:
                    players.append(player_data)
                    if len(players) >= num_players:
                        return players

            if current_page < pages_needed:
                if not self.click_next_page():
                    print(f"Could not load page {current_page + 1}")
                    break
            current_page += 1

        return players

    def wait_for_table(self):
        """Wait for the stats table to load"""
        WebDriverWait(self.driver, WAIT_TIME).until(
            EC.presence_of_element_located((By.CLASS_NAME, "ht-table"))
        )

    def click_next_page(self) -> bool:
        """Click the next page button"""
        try:
            wait = WebDriverWait(self.driver, 10)
            next_button = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a[rel='next']"))
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

