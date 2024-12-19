from dataclasses import dataclass
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By

@dataclass
class Player:
    """Represents a player"""
    jersey_number: str
    name: str
    player_id: str

class GameEvent:
    """Base class for game events"""

    def __init__(self, element: WebElement):
        """Initialize a game event from a row element

        Args:
            element (WebElement): The event row element
        """
        self.element = element
        self.event_type = self._get_event_type()
        self.time = self._get_time()
        self.is_home_team = self._is_home_team()
        self.team_info = self._get_team_info()

    def _get_event_type(self) -> str:
        """Get the event type"""
        return self.element.find_element(By.CSS_SELECTOR, "div.ht-event-type").text

    def _get_time(self) -> str:
        """Get the event time"""
        return self.element.find_element(By.CSS_SELECTOR, "div.ht-event-time span").text

    def _is_home_team(self) -> bool:
        """Check if this is a home team event"""
        home_elements = self.element.find_elements(By.CSS_SELECTOR, "div.ht-hometeam")
        return len(home_elements) > 0

    def _get_team_info(self) -> tuple:
        """Get team information (name, id, logo)"""
        img = self.element.find_element(By.TAG_NAME, "img")
        team_name = img.get_attribute("alt")
        team_logo = img.get_attribute("src")
        team_id = team_logo.split("/")[-1].split("_")[0]
        return (team_name, team_id, team_logo)

    def _parse_player(self, element: WebElement) -> Player:
        """
        Parse player information from various types of play-by-play elements.
    
        Args:
            element: WebElement containing player information
    
        Returns:
            Player: Object containing jersey number, name, and player ID
        """
        try:
            spans = element.find_elements(By.TAG_NAME, "span")
            jersey_number = spans[0].text.replace("#", "")
    
            # Find player link - contains both name and ID
            player_link = element.find_element(By.TAG_NAME, "a")
            href = player_link.get_attribute("href")
            player_id = href.split("/")[-2]  # ID is second to last element in URL
    
            # Find player name - it's in a span inside the link
            name_span = player_link.find_element(By.TAG_NAME, "span")
            name = name_span.text
    
            return Player(
                jersey_number=jersey_number,
                name=name,
                player_id=player_id
            )
        except Exception as e:
            # Handle cases where elements aren't found or are malformed
            raise ValueError(f"Failed to parse player information: {str(e)}")
