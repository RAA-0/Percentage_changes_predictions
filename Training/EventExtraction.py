import json

class EventFeatureExtractor:
    def __init__(self):
        self.non_recurrent_events=[]
        with open('event_config.json') as r:
            event_config=json.load(r)
        for event in event_config.keys():
            if event_config[event]['type']=='variable_dates_events':
                self.non_recurrent_events.append(event)
    def fit(self,X,y=None):
        return self

    def transform(self,X):
        print('extracting...')
        for event in self.non_recurrent_events:
            X[event] = X['event'].apply(lambda events: 1 if event in events else 0)
        return X