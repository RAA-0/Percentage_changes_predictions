from event_type_model.health_event import HealthEvent
from event_type_model.religious_event import ReligiousEvent;
from event_type_model.sports_event import SportsEvent
from event_type_model.season_event import SeasonEvent

class EventFactory:
    @staticmethod
    def create_config(config_type):
        if config_type == "health":
            return HealthEvent()
        elif config_type == "religious":
            return ReligiousEvent()
        elif config_type == "sports":
            return SportsEvent()
        elif config_type == "season":
            return SeasonEvent()
        
        else:
            return None 
