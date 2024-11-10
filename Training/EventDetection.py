from event_type_model.events_factory import EventFactory
from path_config.paths_config import PathConfig
import pandas as pd 


class EventDetector:
    def __init__(self):
        self.f = EventFactory()
        self.conf = PathConfig()
    def fit(self,X,y=None):
        return self
    def transform(self,X):
        event_list=[]
        events =["health","religious","season"]
        for _,row in X.iterrows():
            e=[]
            for event in events:
                e_config = self.f.create_config(event)
                e.extend(e_config.detect_event(pd.to_datetime(row['ds'])))
            event_list.append(e)
        X['event']=event_list
        X[['ds','event']].to_csv("event_detectd.csv",index=False)
        return X[['ds','event']]
        
