import json

class EventFeatureExtractor:
    def __init__(self):
        self.non_recurrent_events=[]
        with open('event_config.json') as r:
            event_config=json.load(r)
        for event in event_config.keys():
            if event_config[event]['type']=='variable_dates_events':
                self.non_recurrent_events.append(event)

    def extract(self,data):
        print('extractingg...')
        for event in self.non_recurrent_events:
            data[event] = data['event'].isin([event]).astype(int)
        return data 