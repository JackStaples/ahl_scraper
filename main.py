from typing import List
from scraper.pages.game_center.plays.game_play import GameEvent
from scraper.pages.game_center.plays.goal_event import GoalEvent
from scraper.pages.game_center.plays.goalie_change_event import GoalieChangeEvent
from scraper.pages.game_center.plays.penalty_event import PenaltyEvent
from scraper.pages.game_center.plays.shot_event import ShotEvent
from scraper.pages.schedule.elements.game_row import GameRow
from scraper.pages.schedule.schedule_page import SchedulePage
from scraper.web_driver_manager import WebDriverManager

def main():
    print("Starting scrape...")
    driver = WebDriverManager.create_driver(headless=False)
    schedule_page = SchedulePage(driver)

    try:
        schedule_page.navigate_to_all_months()
        games = schedule_page.get_games()
        print(f"\nFound {len(games)} games")

        for index, game in enumerate(games[:1], 1):
            print(f"\nScraping game {index} of {len(games)}")
            game = schedule_page.get_game(index)

            if (game.get_game_is_completed()):
                events = get_game_plays(game)
                for event in events:
                    print(event) 

            # if not at last game, navigate back to all months
            if index + 1 < len(games):    
                schedule_page.navigate_to_all_months()

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        print("\nCompleting scrape...")
        driver.quit()

def get_game_plays(game: GameRow) -> List[GameEvent]:
    game_center = game.navigate_to_game_center()
    events = game_center.get_events()
    return events

if __name__ == "__main__":
    main()
