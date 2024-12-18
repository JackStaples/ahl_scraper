from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from typing import List, Tuple
import time

from scraper.pages.schedule.elements.game_row import GameRow

from ..base_page import BasePage
from config import BASE_URL

class SchedulePage(BasePage):
    # Locators
    TABLE_LOCATOR = (By.CLASS_NAME, "ht-table")
    SEASON_SELECT_LOCATOR = (By.CSS_SELECTOR, "select[ng-model='selectedSeason']")
    TEAM_SELECT_LOCATOR = (By.CSS_SELECTOR, "select[ng-model='selectedTeam']")
    MONTH_SELECT_LOCATOR = (By.ID, "ht-month")
    GAME_ROWS_LOCATOR = (By.CSS_SELECTOR, "tr:not(tr:first-child)")  # All rows except header

    PAGE_URL = BASE_URL + "/stats/schedule"

    def navigate_to(self):
        """Navigate to the schedule page"""
        self.driver.get(self.PAGE_URL)
        self.wait_for_table()

    def wait_for_table(self):
        """Wait for the schedule table to load"""
        self.find_element(self.TABLE_LOCATOR)

    def select_season(self, season_id: str) -> bool:
        """Select a season from the dropdown

        Args:
            season_id (str): the season ID to select

        Returns:
            bool: True if season was selected, False otherwise
        """        
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

    def select_team(self, team_id: str) -> bool:
        """Select a team from the dropdown"

        Args:
            team_id (str): team ID to select

        Returns:
            bool: True if team was selected, False otherwise
        """        
        try:
            select_element = self.find_element(self.TEAM_SELECT_LOCATOR)

            self.driver.execute_script(
                """
                var select = arguments[0];
                select.value = arguments[1];
                angular.element(select).triggerHandler('change');
                """, 
                select_element, 
                team_id
            )

            time.sleep(1)
            self.wait_for_table()
            return True

        except Exception as e:
            print(f"Error selecting team: {e}")
            return False

    def select_month(self, month_id: str) -> bool:
        """Select a month from the dropdown

        Args:
            month_id (str): month ID to select

        Returns:
            bool: True if month was selected, False otherwise
        """        
        try:
            select_element = self.find_element(self.MONTH_SELECT_LOCATOR)

            self.driver.execute_script(
                """
                var select = arguments[0];
                select.value = arguments[1];
                angular.element(select).triggerHandler('change');
                """, 
                select_element, 
                month_id
            )

            time.sleep(1)
            self.wait_for_table()
            return True

        except Exception as e:
            print(f"Error selecting month: {e}")
            return False
    
    def get_available_months(self) -> List[Tuple[str, str]]:
        """Get all available months and their IDs

        Returns:
            List[Tuple[str, str]]: List of tuples containing (month_name, month_id)
        """        
        try:
            select_element = self.find_element(self.MONTH_SELECT_LOCATOR)
            options = select_element.find_elements(By.TAG_NAME, "option")
            return [(option.get_attribute("label"), option.get_attribute("value")) 
                   for option in options]
        except Exception as e:
            print(f"Error getting months: {e}")
            return []

    def get_available_seasons(self) -> List[Tuple[str, str]]:
        """Get all available seasons and their IDs

        Returns:
            List[Tuple[str, str]]: List of tuples containing (season_name, season_id)
        """        
        try:
            select_element = self.find_element(self.SEASON_SELECT_LOCATOR)
            options = select_element.find_elements(By.TAG_NAME, "option")
            return [(option.get_attribute("label"), option.get_attribute("value")) 
                   for option in options]
        except Exception as e:
            print(f"Error getting seasons: {e}")
            return []

    def get_available_teams(self) -> List[Tuple[str, str]]:
        """
        Get all available teams and their IDs
        Returns:
            List of tuples containing (team_name, team_id)
        """
        try:
            select_element = self.find_element(self.TEAM_SELECT_LOCATOR)
            options = select_element.find_elements(By.TAG_NAME, "option")
            return [(option.get_attribute("label"), option.get_attribute("value")) 
                   for option in options]
        except Exception as e:
            print(f"Error getting teams: {e}")
            return []

    def get_game_rows(self) -> List[WebElement]:
        """Get all game rows from the current page

        Returns:
            List[WebElement]: List of all game rows
        """        
        table = self.find_element(self.TABLE_LOCATOR)
        return table.find_elements(*self.GAME_ROWS_LOCATOR)
    
    def get_games(self) -> List[GameRow]:
        """Get all games from the current page as GameRow objects
    
        Returns:
            List[GameRow]: List of GameRow objects representing each game
        """        
        rows = self.get_game_rows()
        return [GameRow(row, self.driver) for row in rows]
