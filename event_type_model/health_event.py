from event_type_model.abstract_event import AbstractEvent
import pandas as pd 
from datetime import date
from Scraping.Global_health.mainscraper import main 

class HealthEvent(AbstractEvent):
    def __init__(self):
        super().__init__()
    @property
    def event(self):
        return 'health'    

    def detect_event(self,date):
        events=[]
        if main(date)==1:
            events.append("corona")
        return events 
    
    def get_percentage_changes(self,year,start_date,end_date):
        
        if start_date is None:
            return [0,0]
        percentage_changes = []
        for path in self.data_path:
            df = pd.read_csv(path)
            df['SIBT'] = pd.to_datetime(df["SIBT"])
            df['date'] = df['SIBT'].dt.date
            df['date'] = pd.to_datetime(df['date'])
            df_corona = df[df["date"].dt.year.isin([year])]
            df_no_corona =df[df["date"].dt.year.isin([year-1])]
            df_corona.loc[(df['date'] >= pd.to_datetime(start_date).to_datetime64()) & (df['date'] <= pd.to_datetime(end_date).to_datetime64()), 'is_corona'] = 1

            aveg_corona = df_corona[df_corona['is_corona'] == 1]['TOTAL_TOTAL'].mean()
            aveg_no_corona = df_no_corona['TOTAL_TOTAL'].mean()
            print(f"Average Passengers During corona: {aveg_corona:.2f}")
            print(f"Average Passengers During Non-corona: {aveg_no_corona:.2f}")
            difference = aveg_corona-aveg_no_corona
            percentage_change = (difference/aveg_no_corona)*100
            print(f"percentage_change: {percentage_change}")
            percentage_changes.append(percentage_change)
        return percentage_changes
 