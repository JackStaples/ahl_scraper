from typing import List, Optional
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By

from scraper.pages.game_center.plays.game_play import GamePlay, Player

class GoalPlay(GamePlay):
    """Represents a goal play"""

    def __init__(self, element: WebElement):
        super().__init__(element, 'Goal')
        self.scorer = self._get_scorer()
        self.assists = self._get_assists()
        self.is_power_play = self._is_power_play()
        self.is_insurance_goal = self._is_insurance_goal()

    def __str__(self) -> str:
        assist_text = self.assists[0].name if self.assists else 'no one'
        return f"Goal at {self.time} by {self.scorer.name} assisted by {assist_text}"

    def _get_scorer(self) -> Optional[Player]:
        """Get the scoring player"""
        try:
            details_div = self.element.find_element(
                By.CSS_SELECTOR, 
                self.EVENT_SELECTOR
            )
            # The scorer is the first player in the details
            spans = details_div.find_elements(By.TAG_NAME, "span")
            jersey_number = spans[0].text.replace("#", "")

            player_link = details_div.find_element(By.TAG_NAME, "a")
            href = player_link.get_attribute("href")
            player_id = href.split("/")[-2]
            name = player_link.text

            return Player(
                jersey_number=jersey_number,
                name=name,
                player_id=player_id
            )
        except Exception as e:
            print(f"Error getting scorer: {e}")
            return None

    def _get_assists(self) -> List[Player]:
        """Get the players who assisted on the goal"""
        assists = []
        try:
            details_div = self.element.find_element(
                By.CSS_SELECTOR, 
                self.EVENT_SELECTOR
            )
            assist_elements = details_div.find_elements(
                By.CSS_SELECTOR,
                "span[ng-repeat='assist in pbp.details.assists track by $index']"
            )

            for assist_element in assist_elements:
                spans = assist_element.find_elements(By.TAG_NAME, "span")
                jersey_number = spans[0].text.replace("#", "")

                player_link = assist_element.find_element(By.TAG_NAME, "a")
                href = player_link.get_attribute("href")
                player_id = href.split("/")[-2]
                name = player_link.text

                assists.append(Player(
                    jersey_number=jersey_number,
                    name=name,
                    player_id=player_id
                ))
        except Exception as e:
            print(f"Error getting assists: {e}")
        return assists

    def _is_power_play(self) -> bool:
        """Check if the goal was scored on a power play"""
        try:
            power_play_marker = self.element.find_element(
                By.CSS_SELECTOR,
                "span.ht-gc-marker[ng-if=\"pbp.details.properties.isPowerPlay == '1'\"]"
            )
            return power_play_marker.is_displayed()
        except:
            return False

    def _is_insurance_goal(self) -> bool:
        """Check if the goal was an insurance goal"""
        try:
            insurance_marker = self.element.find_element(
                By.CSS_SELECTOR,
                "span.ht-gc-marker[ng-if=\"pbp.details.properties.isInsuranceGoal == '1'\"]"
            )
            return insurance_marker.is_displayed()
        except:
            return False
