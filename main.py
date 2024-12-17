from scraper.AHLStatsScraper import AHLStatsScraper
from data.DataHandler import DataHandler

def main():
    print("Starting scrape of top 20 AHL scorers...")

    # Initialize scraper and get data
    scraper = AHLStatsScraper()
    try :
        top_100 = scraper.get_players(20)
    finally:
        scraper.close()

    # Handle data display and storage
    DataHandler.display_results(top_100)
    DataHandler.save_to_csv(top_100)
    print("\nFull data saved to 'ahl_top_100_scorers.csv'")

if __name__ == "__main__":
    main()
