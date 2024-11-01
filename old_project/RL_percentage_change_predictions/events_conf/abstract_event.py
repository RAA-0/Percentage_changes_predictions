import json 
from abc import  abstractmethod

class AbstractEvent:
    def __init__(self):
        self.data_path = ["C:\\Users\\Lenovo\\Desktop\\ReinforcementLearning\\FlightML\\FLIGHT_LOAD_ML_202310161702_arrival.csv",
                "C:\\Users\\Lenovo\\Desktop\\ReinforcementLearning\\FlightML\\FLIGHT_LOAD_ML_202310161709_depature.csv"]
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

