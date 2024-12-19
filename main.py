from scraper.pages.game_center.elements.goalie_change_event import GoalieChangeEvent
from scraper.pages.game_center.elements.penalty_event import PenaltyEvent
from scraper.pages.game_center.elements.shot_event import ShotEvent
from scraper.pages.schedule.schedule_page import SchedulePage
from scraper.web_driver_manager import WebDriverManager

def main():
    print("Starting scrape...")
    driver = WebDriverManager.create_driver(headless=False)

    try:
        schedule_page = SchedulePage(driver)
        schedule_page.navigate_to()

        seasons = schedule_page.get_available_seasons()
        months = schedule_page.get_available_months()

        # Let's test with the most recent season and first month
        test_season = seasons[0]  # Most recent season
        test_month = months[0]    # First month in list

        print(f"\nTesting with:")
        print(f"Season: {test_season[0]} (ID: {test_season[1]})")
        print(f"Month: {test_month[0]} (ID: {test_month[1]})")

        # Select the season and month
        schedule_page.select_season(test_season[1])
        schedule_page.select_month(test_month[1])

        # Get games and print info for first 3 games
        games = schedule_page.get_games()
        print(f"\nFound {len(games)} games")

        for i, game in enumerate(games[:1], 1):
            print(f"\nGame {i} of 1:")

            if (game.get_game_is_completed()):
                # Navigate to game center
                game_center = game.navigate_to_game_center()
                
                # Get all events
                events = game_center.get_events()
                
                # Process events
                for event in events:
                    if isinstance(event, ShotEvent):
                        print(f"Shot at {event.time} by {event.shooter.name} on {event.goalie.name}")
                    elif isinstance(event, PenaltyEvent):
                        print(f"Penalty at {event.time} to {event.player.name} - {event.description}")
                    elif isinstance(event, GoalieChangeEvent):
                        print(f"Goalie change at {event.time} - {event.goalie_in.name} in")
                

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        print("\nCompleting scrape...")
        driver.quit()

if __name__ == "__main__":
    main()
