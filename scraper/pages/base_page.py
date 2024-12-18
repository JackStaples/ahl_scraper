from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from typing import Tuple, Any

from config import WAIT_TIME

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, WAIT_TIME)

    def find_element(self, locator: Tuple[By, str]):
        """Wait for and return a single element"

        Args:
            locator (Tuple[By, str]): _description_

        Returns:
            WebElement
        """
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_elements(self, locator: Tuple[By, str]):
        """Wait for and return multiple elements

        Args:
            locator (Tuple[By, str]): _description_

        Returns:
            WebElement[]
        """
        self.wait.until(EC.presence_of_element_located(locator))
        return self.driver.find_elements(*locator)

    def is_element_present(self, locator: Tuple[By, str]) -> bool:
        """Check if an element is present on the page

        Args:
            locator (Tuple[By, str]): _description_

        Returns:
            bool: true if element is present, false otherwise
        """
        try:
            self.find_element(locator)
            return True
        except:
            return False

    def click_element(self, locator: Tuple[By, str]) -> bool:
        """Safely click an element with multiple attempts

        Args:
            locator (Tuple[By, str]): _description_

        Returns:
            bool: returns true if element was clicked, false otherwise
        """
        try:
            element = self.wait.until(EC.element_to_be_clickable(locator))
            try:
                element.click()
            except:
                self.driver.execute_script("arguments[0].click();", element)
            return True
        except Exception as e:
            print(f"Error clicking element: {e}")
            return False

    def scroll_to_element(self, element: Any) -> None:
        """Scroll element into view"

        Args:
            element (Any): the element to scroll to
        """
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
