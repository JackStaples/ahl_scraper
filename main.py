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

        games = schedule_page.get_games()
        print(f"\nFound {len(games)} games")

        for index, game in enumerate(games[:2], 1):
            print(f"\nGame {index} of 1:")
            game = schedule_page.get_game(index)

            if (game.get_game_is_completed()):
                game_center = game.navigate_to_game_center()
                events = game_center.get_events()
                for event in events:
                    if isinstance(event, ShotEvent):
                        print(f"Shot at {event.time} by {event.shooter.name} on {event.goalie.name}")
                    elif isinstance(event, PenaltyEvent):
                        print(f"Penalty at {event.time} to {event.player.name} - {event.description}")
                    elif isinstance(event, GoalieChangeEvent):
                        print(f"Goalie change at {event.time} - {event.goalie_in.name} in")
                
            schedule_page.navigate_to()

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        print("\nCompleting scrape...")
        driver.quit()

if __name__ == "__main__":
    main()
