from events_conf.abstract_event import AbstractEvent
import pandas as pd 
from datetime import date
from hijri_converter import Hijri, Gregorian

class RamadanEvent(AbstractEvent):
    def __init__(self):
        super().__init__()
    
    @property
    def event(self):
        return 'ramadan_season'

    def get_dates(self,year):
        hijri_year = Gregorian(year, 1, 1).to_hijri().year  
        
        ramadan_start_hijri = Hijri(hijri_year, 9, 1)  
        ramadan_month_length = ramadan_start_hijri.month_length() 
        ramadan_end_hijri = Hijri(hijri_year, 9, ramadan_month_length)    
        
        ramadan_start_gregorian = ramadan_start_hijri.to_gregorian()
        ramadan_end_gregorian = ramadan_end_hijri.to_gregorian()
        
        return ramadan_start_gregorian, ramadan_end_gregorian
    
    def get_percentage_changes(self,year,start_date,end_date):
        
        percentage_changes=[]
        for path in self.data_path:
            df = pd.read_csv(path)
            df['SIBT'] = pd.to_datetime(df['SIBT'])
            df['date'] = df['SIBT'].dt.date
            df['date'] = pd.to_datetime(df['date'])
            df['is_ramadan'] = None  
            df = df[df["date"].dt.year.isin([year])]

            df.loc[(df['date'] >= pd.to_datetime(start_date)) & (df['date'] <= pd.to_datetime(end_date)), 'is_ramadan'] = 1
            df.loc[(df['date'] < pd.to_datetime(start_date)) , 'is_ramadan'] = 0


            ramadan_data = df[df['is_ramadan'] == 1]  
            non_ramadan_data = df[df['is_ramadan'] == 0]  

            avg_ramadan_passengers = df[df['is_ramadan'] == 1]['TOTAL_TOTAL'].mean()
            avg_non_ramadan_passengers = df[df['is_ramadan'] == 0]['TOTAL_TOTAL'].mean()

            print(f"Average Passengers During ramadan: {avg_ramadan_passengers}")
            print(f"Average Passengers During Non-ramadan: {avg_non_ramadan_passengers}")

            difference = avg_ramadan_passengers - avg_non_ramadan_passengers
            percentage_change = (difference/avg_non_ramadan_passengers)*100
            print(f"percentage_change: {percentage_change}")
            percentage_changes.append(percentage_change)
        return percentage_changes