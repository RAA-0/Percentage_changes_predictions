from event_type_model.abstract_event import AbstractEvent
import pandas as pd 
from datetime import date 

class SeasonEvent(AbstractEvent):
    def __init__(self):
        super().__init__()
      
    def detect_event(self,date):
        events=[]
        seasons = ["summer_season","spring_season"]
        for season in seasons: 
            start,end=self.get_dates(pd.to_datetime(date).year,season) 
            if pd.to_datetime(start)<=pd.to_datetime(date)<=pd.to_datetime(end):
                events.append(season)
        return events 
        

    def get_dates(self,year,season):
        seasons_dates={"summer_season":[(6,1),(9,1)],"spring_season":[(3,20),(4,20)]}
        start_date = date(year,seasons_dates[season][0][0],seasons_dates[season][0][1])
        end_date = date(year,seasons_dates[season][1][0],seasons_dates[season][1][1])
        return start_date,end_date
   
        
        
    
   