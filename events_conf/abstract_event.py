import json 
from abc import  abstractmethod

class AbstractEvent:
    def __init__(self):
        self.read_config_file()

    @property
    def event(self):
       return ''
    @property
    def years(self):
        return self.config[self.event]['years']
    
    @abstractmethod
    def get_dates(self, year):
        pass
    
    @abstractmethod
    def get_percentage_changes(self, year, start_date, end_date):
        pass

    def read_config_file(self):
        with open("event_config.json", "r") as json_file:
            data = json.load(json_file)
        self.config = data
        with open('config.json') as jf:
            paths = json.load(jf)
        self.data_path = [paths['original_arrival_data_path'],paths['original_departure_data_path']]



