import pandas as pd
from prophet import Prophet
import joblib
from sklearn.metrics import r2_score, mean_squared_error
import json
import random

class DataTrainer:
    def __init__(self,data,target):
        self.target=target
        self.data = data
        self.classify_events()
        random.seed(42)
        
    def split_data(self):
        self.data = self.data.sort_values(by='ds')
        train_data = self.data[self.data['ds'] <= '2023-12-01']  
        test_data = self.data[self.data['ds'] > '2023-12-01']
        return train_data,test_data


    def prophet_model(self):
        print(f'building moddell for {self.target}s....')
        prophet_model = Prophet(holidays=self.holidays_data)
        for event in self.non_recurrent_events:
            prophet_model.add_regressor(event)
        return prophet_model
    
    def train(self,model):
        print("training....")
        self.data['start_date'] = pd.to_datetime(self.data['start_date'])
        self.data.rename(columns={'start_date': 'ds', f'{self.target}_percentage_change': 'y'}, inplace=True)
        self.data['ds'] = pd.to_datetime(self.data['ds'])
        train_data, test_data = self.split_data()
        model.fit(train_data)
        self.evaluate_model(model,test_data)
        joblib.dump(model,f'models\\prophet_{self.target}_model.joblib')
        return model
    
    def evaluate_model(self,model,test_data):
        print(f'evaluating {self.target}s model...')
        forecast = model.predict(test_data)
        r2 = r2_score(test_data['y'],forecast['yhat'])
        mse = mean_squared_error(test_data['y'],forecast['yhat'])
        print(f"R2: {r2} \t MSE:{mse}")

    def classify_events(self):
        self.non_recurrent_events = []
        self.holiday_events =[]
        with open('event_config.json') as r:
            event_config=json.load(r)

        for event in event_config.keys():
            if event_config[event]['type']=='variable_dates_events':
                self.non_recurrent_events.append(event)
            if event_config[event]['type']=='fixed_dates_events':
                self.holiday_events.append(event)
                events = self.data[self.data['event'].isin(self.holiday_events)]

        self.holidays_data = pd.DataFrame({
            'holiday': events['event'],
            'ds': events['start_date'],
            'lower_window': 0,
            'upper_window': (pd.to_datetime(events['end_date']) - pd.to_datetime(events['start_date'])).dt.days
        })


