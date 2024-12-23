from enum import Enum
from typing import Optional, Type

from scraper.pages.game_center.plays.game_play import GamePlay
from scraper.pages.game_center.plays.goal_play import GoalPlay
from scraper.pages.game_center.plays.goalie_change_play import GoalieChangePlay
from scraper.pages.game_center.plays.penalty_play import PenaltyPlay
from scraper.pages.game_center.plays.shot_play import ShotPlay

class PlayType(Enum):
    GOALIE_CHANGE = (GoalieChangePlay, "GOALIE CHANGE")
    SHOT = (ShotPlay, "SHOT")
    PENALTY = (PenaltyPlay, "PENALTY")
    GOAL = (GoalPlay, "GOAL")

    def __init__(self, play_class: Type[GamePlay], text: str):
        self.play_class = play_class
        self.text = text

    @classmethod
    def from_text(cls, text: str) -> Optional['PlayType']:
        for play_type in cls:
            if play_type.text in text:
                return play_type
        return None
    
    def create_play(self, element) -> Optional[GamePlay]:
        return self.play_class(element)
