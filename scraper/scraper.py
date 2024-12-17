from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from typing import List, Dict
import time

from config import *
from scraper.web_driver import WebDriverManager
from scraper.parser import PlayerParser

class AHLStatsScraper:
    def __init__(self, headless: bool = True):
        self.driver = WebDriverManager.create_driver(headless)
        self.parser = PlayerParser()

    def __del__(self):
        self.driver.quit()

    def wait_for_table(self):
        """Wait for the stats table to load"""
        WebDriverWait(self.driver, WAIT_TIME).until(
            EC.presence_of_element_located((By.CLASS_NAME, "ht-table"))
        )

    def click_next_page(self) -> bool:
        """Click the next page button"""
        try:
            next_button = self.driver.find_element(By.CSS_SELECTOR, "a[rel='next']")
            actions = ActionChains(self.driver)
            actions.move_to_element(next_button).click().perform()
            return True
        except:
            return False

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
