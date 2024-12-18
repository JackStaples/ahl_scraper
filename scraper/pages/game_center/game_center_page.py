from selenium.webdriver.common.by import By
import time

from scraper.pages.game_center.elements.event_factory import EventFactory

from ..base_page import BasePage

class GameCenterPage(BasePage):
    # Locators
    PERIOD_SECTIONS_LOCATOR = (By.CSS_SELECTOR, ".ht-play-by-play > div > div:nth-child(3)")
    EVENT_ROWS_LOCATOR = (By.CSS_SELECTOR, "div.ht-event-row")

    def wait_for_load(self):
        """Wait for the game center page to load"""
        self.wait_for_element_visible(self.PERIOD_SECTIONS_LOCATOR)
        time.sleep(1)  # Give extra time for events to load

    def get_events(self):
        """Get all events from the game"""
        events = []

        event_elements = self.driver.find_elements(
            By.CSS_SELECTOR, 
            "div.ht-event-row"
        )

        for element in event_elements:
            event = EventFactory.create_event(element)
            if event:
                events.append(event)

        return events