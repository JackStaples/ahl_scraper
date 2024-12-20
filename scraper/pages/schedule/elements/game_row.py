from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from dataclasses import dataclass
from typing import Optional
from datetime import datetime

from scraper.pages.game_center.game_center_page import GameCenterPage

@dataclass
class Team:
    """Represents a team in a game"""
    name: str
    id: str
    logo_url: str
    score: int

class GameRow:
    """Represents a row in the schedule table"""

    def __init__(self, row_element: WebElement, driver):
        self.row = row_element
        self.driver = driver

    def get_date(self) -> str:
        """Get the date the game occurred

        Returns:
            str: The date in the format 'Mon, Jan 01'
        """        
        date_cell = self.row.find_element(By.CSS_SELECTOR, "td.date_with_day span")
        return date_cell.text

    def get_parsed_date(self) -> datetime:
        """Get the game date as a datetime object

        Returns:
            datetime: The game date
        """        
        date_str = self.get_date()
        return datetime.strptime(date_str, "%a, %b %d")

    def get_status(self) -> str:
        """Get the game status (e.g., 'Final', 'Final SO', etc.)

        Returns:
            str: The game status
        """        
        status_cell = self.row.find_element(By.CSS_SELECTOR, "td.game_status span")
        return status_cell.text

    def get_visiting_team(self) -> Team:
        """Get visiting team information

        Returns:
            Team: The visiting team
        """        
        cell = self.row.find_element(By.CSS_SELECTOR, "td.visiting_team_city")
        link = cell.find_element(By.TAG_NAME, "a")
        team_id = link.get_attribute("href").split("/")[-2]
        logo = cell.find_element(By.TAG_NAME, "img")
        score_cell = self.row.find_element(By.CSS_SELECTOR, "td.visiting_goal_count span")

        return Team(
            name=link.text,
            id=team_id,
            logo_url=logo.get_attribute("src"),
            score=int(score_cell.text) if score_cell.text else 0
        )

    def get_home_team(self) -> Team:
        """Get home team information

        Returns:
            Team: The home team
        """        
        cell = self.row.find_element(By.CSS_SELECTOR, "td.home_team_city")
        link = cell.find_element(By.TAG_NAME, "a")
        team_id = link.get_attribute("href").split("/")[-2]
        logo = cell.find_element(By.TAG_NAME, "img")
        score_cell = self.row.find_element(By.CSS_SELECTOR, "td.home_goal_count span")

        return Team(
            name=link.text,
            id=team_id,
            logo_url=logo.get_attribute("src"),
            score=int(score_cell.text) if score_cell.text else 0
        )

    def get_game_center_url(self) -> Optional[str]:
        """Get the game center URL if availableGet the game center URL if available

        Returns:
            Optional[str]: The game center URL
        """        
        try:
            link = self.row.find_element(By.CSS_SELECTOR, "td.game_center a")
            return link.get_attribute("href")
        except:
            return None

    def get_game_sheet_url(self) -> Optional[str]:
        """Get the game sheet URL if available

        Returns:
            Optional[str]: The game sheet URL
        """        
        try:
            link = self.row.find_element(By.CSS_SELECTOR, "td.game_sheet a")
            return link.get_attribute("href")
        except:
            return None

    def get_game_report_url(self) -> Optional[str]:
        """Get the game report URL if available

        Returns:
            Optional[str]: The game report URL
        """        
        try:
            link = self.row.find_element(By.CSS_SELECTOR, "td.game_report a")
            return link.get_attribute("href")
        except:
            return None

    def get_game_summary_url(self) -> Optional[str]:
        """Get the game summary URL if available

        Returns:
            Optional[str]: The game summary URL
        """        
        try:
            link = self.row.find_element(By.CSS_SELECTOR, "td.game_summary_long a")
            return link.get_attribute("href")
        except:
            return None
        
    def get_game_is_completed(self) -> bool:
        """Check if the game is completed

        Returns:
            bool: True if the game is completed, False otherwise
        """        
        return self.get_status().lower().startswith("final")
    
    def navigate_to_game_center(self) -> 'GameCenterPage':
        """Click the game center link and return a new GameCenterPage instance

        Returns:
            GameCenterPage: The game center page for this game
        """
        game_center_link = self.row.find_element(By.CSS_SELECTOR, "td.game_center a")
        game_center_link.click()
        return GameCenterPage(self.driver)

