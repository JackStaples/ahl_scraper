import pandas as pd
from typing import List, Dict
from config import DEFAULT_FILENAME

class DataHandler:
    @staticmethod
    def save_to_csv(data: List[Dict], filename: str = DEFAULT_FILENAME):
        """Save data to CSV file"""
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False)
        print(f"Data saved to {filename}")

    @staticmethod
    def display_results(data: List[Dict]):
        """Display results in a formatted way"""
        df = pd.DataFrame(data)
        print(f"\nRetrieved {len(data)} players")
        print("\nScorers:")
        print(df[['rank', 'name', 'team', 'gp', 'goals', 'assists', 'points']])
