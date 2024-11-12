import pandas as pd 
from datetime import date, timedelta
from hijri_converter import Hijri, Gregorian

class ReligiousEvent():
    def __init__(self):
        self.islamic_holidays = {"ramadan_season":[(9, 1),(9, 30)],"hajj_season":[(12,5),(12,15)],"eid_al_fitr":[(10, 1), (10, 3)],"eid_al_adha": [(12, 10), (12, 13)]}
        self.seasons_dates={"summer_season":[(6,1),(9,1)],"spring_season":[(3,20),(4,20)],"christmas_season":[(12,23),(12,30)],"new_years_break":[(12,31),(1,6)]} 
      
    def detect_event(self,date):
        events=[]
        for holiday in self.islamic_holidays.keys(): 
            start,end=self.get_dates_(pd.to_datetime(date).year,holiday) 
            if pd.to_datetime(start)<=pd.to_datetime(date)<=pd.to_datetime(end):
                events.append(holiday)
            if holiday=="hajj":
                if pd.to_datetime(start)- timedelta(days=4)<=pd.to_datetime(date)<pd.to_datetime(start):
                    events.append("pre_hajj_season")
        for fixed_holiday in self.seasons_dates.keys():
            start,end = self.get_dates(pd.to_datetime(date).year,fixed_holiday)
            if  pd.to_datetime(start)<=pd.to_datetime(date)<=pd.to_datetime(end):
                events.append(fixed_holiday)
        return events 


    def get_dates_(self,year,holiday):
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
    
    def get_dates(self,year,season):
        start_date = date(year,self.seasons_dates[season][0][0],self.seasons_dates[season][0][1])
        end_date = date(year,self.seasons_dates[season][1][0],self.seasons_dates[season][1][1])
        if season == 'new_years_break':
            end_date = date(year+1,self.seasons_dates[season][1][0],self.seasons_dates[season][1][1])
        return start_date,end_date
        
        
    
   