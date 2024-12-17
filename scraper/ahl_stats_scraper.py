from typing import List, Dict

from config import BASE_URL, PLAYERS_PER_PAGE
from scraper.web_driver_manager import WebDriverManager
from scraper.player_parser import PlayerParser
from scraper.pages.player_stats_page import PlayerStatsPage

class AHLStatsScraper:
    def __init__(self, headless: bool = True):
        self.driver = WebDriverManager.create_driver(headless)
        self.parser = PlayerParser()
        self.stats_page = PlayerStatsPage(self.driver)

    def __del__(self):
        self.close()

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
        self.stats_page.navigate_to()

        players = []
        pages_needed = num_players // PLAYERS_PER_PAGE
        current_page = 1

        while current_page <= pages_needed:
            print(f"Scraping page {current_page}...")

            rows = self.stats_page.get_player_rows()
            for row in rows:
                player_data = self.parser.parse_player_row(row)
                if player_data:
                    players.append(player_data)
                    if len(players) >= num_players:
                        return players

            if current_page < pages_needed:
                if not self.stats_page.click_next_page():
                    print(f"Could not load page {current_page + 1}")
                    break
            current_page += 1

        return players
