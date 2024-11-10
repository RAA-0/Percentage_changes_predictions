from event_type_model.abstract_event import AbstractEvent
import pandas as pd 
from datetime import date, timedelta
from hijri_converter import Hijri, Gregorian

class ReligiousEvent(AbstractEvent):
    def __init__(self):
        super().__init__()
        self.islamic_holidays = {"ramadan_season":[(9, 1),(9, 30)],"hajj_season":[(12,5),(12,15)],"eid_al_fitr":[(10, 1), (10, 3)],"eid_al_adha": [(12, 10), (12, 13)]}
    @property
    def event(self):
        return 'pre_hajj_season' 
      
    def detect_event(self,date):
        events=[]
        holidays = ["ramadan_season","hajj_season","eid_al_fitr","eid_al_adha"]
        for holiday in holidays: 
            start,end=self.get_dates(pd.to_datetime(date).year,holiday) 
            if pd.to_datetime(start)<=pd.to_datetime(date)<=pd.to_datetime(end):
                events.append(holiday)
            if holiday=="hajj":
                if pd.to_datetime(start)- timedelta(days=4)<=pd.to_datetime(date)<pd.to_datetime(start):
                    events.append("pre_hajj_season")
        ch_start,ch_end,ny_start,ny_end = self.get_christmas_dates(pd.to_datetime(date).year)
        if  pd.to_datetime(ch_start)<=pd.to_datetime(date)<=pd.to_datetime(ch_end):
            events.append("christmas_season")
        elif pd.to_datetime(ny_start)<=pd.to_datetime(date)<=pd.to_datetime(ny_end):
            if pd.to_datetime(ny_start)==pd.to_datetime(date):events.append("new_years_eve")
            else: events.append("new_years_break")
        return events 
        



        

    def get_dates(self,year,holiday):
        hijri_date = Gregorian(year, 1, 1).to_hijri() 
        try:   
            start_hijri = Hijri(hijri_date.year, self.islamic_holidays[holiday][0][0], self.islamic_holidays[holiday][0][1])
            
        except:
            start_hijri = Hijri(hijri_date.year,self.islamic_holidays[holiday][0][0], 29)
        try:
            end_hijri = Hijri(hijri_date.year,self.islamic_holidays[holiday][1][0], self.islamic_holidays[holiday][1][1])
        except:
            end_hijri = Hijri(hijri_date.year,self.islamic_holidays[holiday][1][0], 29)


        start_gregorian = start_hijri.to_gregorian()
        end_gregorian = end_hijri.to_gregorian()
  
        return start_gregorian, end_gregorian
    def get_christmas_dates(self,year):
        christmas_start_date = date(year,12,23)
        christmas_end_date = date(year,12,30)
        new_year_start_date = date(year,12,31)
        new_year_end_date = date(year+1,1,6)
        return christmas_start_date,christmas_end_date,new_year_start_date,new_year_end_date
        
        
    
   