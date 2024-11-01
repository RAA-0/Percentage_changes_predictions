from events_conf.abstract_event import AbstractEvent
import pandas as pd 
from datetime import date, timedelta
from hijri_converter import Hijri, Gregorian

class HajjEvent(AbstractEvent):
    def __init__(self):
        super().__init__()
    @property
    def event(self):
        return 'pre_hajj_season'    

    def get_dates(self,year):
        hijri_date = Gregorian(year, 1, 1).to_hijri()    
        hajj_start_hijri = Hijri(hijri_date.year, 12, 5) #expanded to take intoaccount travel floghts before and after 
        hajj_end_hijri = Hijri(hijri_date.year, 12, 15)

        hajj_start_gregorian = hajj_start_hijri.to_gregorian()
        hajj_end_gregorian = hajj_end_hijri.to_gregorian()
        pre_hajj_start_gregorian = hajj_start_gregorian - timedelta(days=4)
        
        pre_hajj_end_gregorian = hajj_start_gregorian
        
        return pre_hajj_start_gregorian, pre_hajj_end_gregorian        
        
    
    def get_percentage_changes(self,year,start_date,end_date):
        
        start_date = pd.to_datetime('2023-06-20')
        end_date = pd.to_datetime('2023-06-26')
        percentage_changes = []
        for path in self.data_path:
            typ = path[-11:-3]
            df = pd.read_csv(path)
            df['SIBT'] = pd.to_datetime(df['SIBT'])
            df['date'] = df['SIBT'].dt.date
            df['date'] = pd.to_datetime(df['date'])
            df = df[df["date"].dt.year.isin([year])
                    &
            ((df["ORIGINICAO"] == "OEJN") | (df["DESTINATIONICAO"] == "OEJN"))]
            df['date'] = df['SIBT'].dt.date
            df['is_hajj'] = None
            df.loc[(df['date'] >= pd.to_datetime(start_date).date()) & (df['date'] <= pd.to_datetime(end_date).date()), 'is_hajj'] = 1
            df.loc[(df['date'] > pd.to_datetime(end_date).date()), 'is_hajj'] = 0
  

            avg_hajj_passengers = df[df['is_hajj'] == 1]['TOTAL_TOTAL'].mean()
            avg_non_hajj_passengers = df[df['is_hajj'] == 0]['TOTAL_TOTAL'].mean()
            print(f'{typ}')
            print(f"Average Passengers During Hajj: {avg_hajj_passengers}")
            print(f"Average Passengers During Non-Hajj: {avg_non_hajj_passengers}")

            difference = avg_hajj_passengers - avg_non_hajj_passengers
            percentage_change = (difference/avg_non_hajj_passengers)*100
            print(f"percentage_change: {percentage_change}")
            percentage_changes.append(percentage_change)
        return percentage_changes
 