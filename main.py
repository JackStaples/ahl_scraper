from scraper.pages.schedule.schedule_page import SchedulePage
from scraper.web_driver_manager import WebDriverManager
from typing import Tuple

def print_game_info(game_row, season: Tuple[str, str], month: Tuple[str, str]) -> None:
    """Print formatted information about a game"""
    try:
        visiting_team = game_row.get_visiting_team()
        home_team = game_row.get_home_team()

        print(f"\nGame Details ({season[0]} - {month[0]}):")
        print(f"  Date: {game_row.get_date()}")
        print(f"  Status: {game_row.get_status()}")
        print(f"  Matchup: {visiting_team.name} ({visiting_team.score}) @ {home_team.name} ({home_team.score})")

        # Print available links
        game_center = game_row.get_game_center_url()
        if game_center:
            print(f"  Game Center: {game_center}")

        game_sheet = game_row.get_game_sheet_url()
        if game_sheet:
            print(f"  Game Sheet: {game_sheet}")

        game_report = game_row.get_game_report_url()
        if game_report:
            print(f"  Game Report: {game_report}")

    except Exception as e:
        print(f"Error processing game: {e}")

def main():
    print("Starting scrape...")
    driver = WebDriverManager.create_driver()

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

        for i, game in enumerate(games[:3], 1):
            print(f"\nGame {i} of 3:")
            print_game_info(game, test_season, test_month)

        # Optional: Test with a specific team
        teams = schedule_page.get_available_teams()
        if teams:
            test_team = teams[0]  # First team in list
            print(f"\nTesting team filter with: {test_team[0]}")
            schedule_page.select_team(test_team[1])

            team_games = schedule_page.get_games()
            print(f"Found {len(team_games)} games for {test_team[0]}")
            if team_games:
                print_game_info(team_games[0], test_season, test_month)

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        print("\nCompleting scrape...")
        driver.quit()

if __name__ == "__main__":
    main()
