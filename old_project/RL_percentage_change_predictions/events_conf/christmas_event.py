from events_conf.abstract_event import AbstractEvent; 
import pandas as pd 
from datetime import date

class ChristmasEvent(AbstractEvent):
    def __init__(self):
        super().__init__()
    
    @property
    def event(self):
        return 'christmas_season'

    def get_dates(self,year):
        start_date = date(year,12,23)
        end_date = date(year+1,1,6)
        return start_date, end_date
        
    def get_percentage_changes(self,year,start_date,end_date):
 
        percentage_changes=[]
        chrismtas_holiday_start_date = date(year,12,23)
        christmas_holiday_end_date = date(year,12,31)
        newyear_holiday_start_date = date(year,1,1)
        newyear_holiday_end_date = date(year,1,6)
        for path in self.data_path:
            df = pd.read_csv(path)
            df['SIBT'] = pd.to_datetime(df['SIBT'])
            df['date'] = df['SIBT'].dt.date
            df['date'] = pd.to_datetime(df['date'])
            df = df[df["date"].dt.year.isin([year])]
            df['date'] = df['SIBT'].dt.date
            df['is_christmas'] = 0 

            df.loc[(df['date'] >= pd.to_datetime(chrismtas_holiday_start_date).date()) & (df['date'] <= pd.to_datetime(christmas_holiday_end_date).date()), 'is_christmas'] = 1
            df.loc[(df['date'] >= pd.to_datetime(newyear_holiday_start_date).date()) & (df['date'] <= pd.to_datetime(newyear_holiday_end_date).date()), 'is_christmas'] = 1

            hajj_data = df[df['is_christmas'] == 1]  
            non_hajj_data = df[df['is_christmas'] == 0]  

            avg_christmas_passengers = df[df['is_christmas'] == 1]['TOTAL_TOTAL'].mean()
            avg_non_christmas_passengers = df[df['is_christmas'] == 0]['TOTAL_TOTAL'].mean()

            print(f"Average Passengers During christams: {avg_christmas_passengers}")
            print(f"Average Passengers During Non-christmas: {avg_non_christmas_passengers}")

            difference = avg_christmas_passengers - avg_non_christmas_passengers
            percentage_change = (difference/avg_non_christmas_passengers)*100
            print(f"percentage_change: {percentage_change}")

            percentage_changes.append(percentage_change)
        return percentage_changes