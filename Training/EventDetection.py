from event_type_model.news_event import NewsEvent
from event_type_model.religious_event import ReligiousEvent
from path_config.paths_config import PathConfig
import pandas as pd 


class EventDetector:
    def __init__(self):
        self.conf = PathConfig()
        self.ne = NewsEvent()
        self.re = ReligiousEvent()

    def fit(self,X,y=None):
        return self
    
    def transform(self,X):
        event_list=[]
        classes = [self.re,self.ne]
        for _,row in X.iterrows():
            e=[]
            for e_config in classes:
                e.extend(e_config.detect_event(pd.to_datetime(row['ds'])))
            event_list.append(e)
        X['event']=event_list
        X[['ds','event']].to_csv("data\\Serving\\events_detected.csv",index=False)
        return X[['ds','event']]
        
