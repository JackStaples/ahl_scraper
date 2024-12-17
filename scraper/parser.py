from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from typing import Dict, Optional

class PlayerParser:
    @staticmethod
    def parse_player_row(row: WebElement) -> Optional[Dict]:
        """Parse a single player row"""
        cells = row.find_elements(By.TAG_NAME, "td")
        if len(cells) < 15:
            return None

        return {
            'rank': cells[0].text.strip(),
            'name': cells[3].text.strip(),
            'position': cells[4].text.strip(),
            'team': cells[5].text.strip(),
            'gp': cells[6].text.strip(),
            'goals': cells[7].text.strip(),
            'assists': cells[8].text.strip(),
            'points': cells[9].text.strip(),
            'plus_minus': cells[10].text.strip(),
            'pim': cells[11].text.strip(),
            'ppg': cells[12].text.strip(),
            'shg': cells[13].text.strip(),
            'points_per_game': cells[14].text.strip(),
            'pim_per_game': cells[15].text.strip(),
            'shots': cells[16].text.strip()
        }
