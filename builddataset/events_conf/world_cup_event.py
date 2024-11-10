from events_conf.abstract_event import AbstractEvent
import pandas as pd 
from datetime import date
from hijri_converter import Hijri, Gregorian

class WorldCupEvent(AbstractEvent):
    def __init__(self):
        super().__init__()
    
    @property
    def event(self):
        return 'world_cup'

    def get_dates(self,year):
        start_date =date(year,11,17)
        end_date = date(year,12,19)
        return start_date, end_date
    
    def get_percentage_changes(self,year,start_date,end_date):
        percentage_changes=[]
        for path in self.data_path:
            typ = path[-11:-3]
            df = pd.read_csv(path)
            df['SIBT'] = pd.to_datetime(df['SIBT'])
            df['date'] = df['SIBT'].dt.date
            df['date'] = pd.to_datetime(df['date'])
            df['is_wc'] = None  
            df = df[df["date"].dt.year.isin([year])]
            #&
            #(df["ORIGINICAO"].isin(qa_icao_codes))| (df["DESTINATIONICAO"].isin(qa_icao_codes))]
            #print(df[["ORIGINICAO","DESTINATIONICAO"]])

            df.loc[(df['date'] >= pd.to_datetime(start_date)) & (df['date'] <= pd.to_datetime(end_date)), 'is_wc'] = 1
            df.loc[(df['date'] > pd.to_datetime(end_date)) , 'is_wc'] = 0


            ramadan_data = df[df['is_wc'] == 1]  
            non_ramadan_data = df[df['is_wc'] == 0]  

            avg_ramadan_passengers = df[df['is_wc'] == 1]['TOTAL_TOTAL'].mean()
            avg_non_ramadan_passengers = df[df['is_wc'] == 0]['TOTAL_TOTAL'].mean()

            print(f"Average Passengers During world cup season {avg_ramadan_passengers}")
            print(f"Average Passengers with no world cup: {avg_non_ramadan_passengers}")

            difference = avg_ramadan_passengers - avg_non_ramadan_passengers
            percentage_change = (difference/avg_non_ramadan_passengers)*100
            print(f"percentage_change: {percentage_change}")
            percentage_changes.append(percentage_change)
        return percentage_changes