from events_conf.corona_event import CoronaEvent;
from events_conf.christmas_event import ChristmasEvent;
from events_conf.ramadan_event import RamadanEvent;
from events_conf.hajj_event import HajjEvent;
from events_conf.world_cup_event import WorldCupEvent

class EventFactory:
    @staticmethod
    def create_config(config_type):
        if config_type == "corona":
            return CoronaEvent()
        elif config_type == "ramadan":
            return RamadanEvent()
        elif config_type == "hajj":
            return HajjEvent()
        elif config_type == "christmas":
            return ChristmasEvent()
        elif config_type == "world_cup":
            return WorldCupEvent()
        
        else:
            raise ValueError("Invalid configuration type")
