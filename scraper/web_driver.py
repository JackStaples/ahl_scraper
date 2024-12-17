from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class WebDriverManager:
    @staticmethod
    def create_driver(headless: bool = True) -> webdriver.Chrome:
        options = Options()
        if headless:
            options.add_argument('--headless')
        return webdriver.Chrome(options=options)
