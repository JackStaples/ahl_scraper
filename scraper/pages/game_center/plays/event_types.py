from enum import Enum
from typing import Optional, Type

from scraper.pages.game_center.plays.game_play import GameEvent
from scraper.pages.game_center.plays.goal_event import GoalEvent
from scraper.pages.game_center.plays.goalie_change_event import GoalieChangeEvent
from scraper.pages.game_center.plays.penalty_event import PenaltyEvent
from scraper.pages.game_center.plays.shot_event import ShotEvent

class EventType(Enum):
    GOALIE_CHANGE = (GoalieChangeEvent, "GOALIE CHANGE")
    SHOT = (ShotEvent, "SHOT")
    PENALTY = (PenaltyEvent, "PENALTY")
    GOAL = (GoalEvent, "GOAL")

    def __init__(self, event_class: Type[GameEvent], text: str):
        self.event_class = event_class
        self.text = text

    @classmethod
    def from_text(cls, text: str) -> Optional['EventType']:
        for event_type in cls:
            if event_type.text in text:
                return event_type
        return None
    
    def create_event(self, element) -> Optional[GameEvent]:
        return self.event_class(element)
