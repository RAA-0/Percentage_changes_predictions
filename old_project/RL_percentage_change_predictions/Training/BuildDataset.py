from events_conf.events_factory import EventFactory
import pandas as pd 

class DatasetBuilder:

    def __init__(self,path):
        self.path =path

    def build_dataset(self):
        print("Building Dataset...")
        corona_config = EventFactory.create_config('corona')
        christmas_config = EventFactory.create_config('christmas')
        ramadan_config = EventFactory.create_config('ramadan')
        hajj_config = EventFactory.create_config('hajj')
        world_cup = EventFactory.create_config('world_cup')
        configurations = [corona_config, christmas_config, ramadan_config, hajj_config,world_cup]
        new_df = pd.DataFrame()
        
        for config in configurations:
            for year in config.years:
                start_date, end_date = config.get_dates(year)
                if start_date and end_date:
                    df = pd.DataFrame({
                        "year":[year],
                        'event':[config.event],
                        "start_date":[str(start_date)],  
                        "end_date":[ str(end_date)],    
                        "arrival_percentage_change": config.get_percentage_changes(year,start_date,end_date)[0],
                        "departure_percentage_change":config.get_percentage_changes(year,start_date,end_date)[1]
                    })
                    new_df=pd.concat([new_df,df])
            """df_non_event = pd.DataFrame({
                        "year": [year],
                        "event": ["no_event"],
                        "start_date":None,
                        "end_date":None,
                        "arrival_percentage_change": [0],  # Assuming no change during non-event periods
                        "departure_percentage_change": [0]
                    })
            new_df = pd.concat([new_df, df_non_event])"""

        new_df.to_csv(self.path,index=False)
        return new_df

