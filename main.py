from scraper.pages.schedule_page import SchedulePage
from scraper.web_driver_manager import WebDriverManager

def main():
    print("Starting scrape...")
    schedulePage = SchedulePage(WebDriverManager.create_driver())
    schedulePage.navigate_to()

    seasons = schedulePage.get_available_seasons()
    # teams = schedulePage.get_available_teams()
    months = schedulePage.get_available_months()

    for season in seasons:
        for month in months:
            print(f"Scraping {season} - {month}")


    print("\nCompleting scrape...")

if __name__ == "__main__":
    main()
