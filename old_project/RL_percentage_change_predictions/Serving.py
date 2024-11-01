import pandas as pd
from stable_baselines3 import PPO, DDPG, A2C
import numpy as np 
from Training.new_model import Model

#check the r2 score 

event_configuration = pd.read_csv('data\\Training\\TrainingDataset.csv')


def new_prediction(row):
    year = int(row['date_time_year'])
    month = int(row['date_time_month'])
    day = int(row['date_time_day_of_month'])
    date = pd.to_datetime({'year': [year], 'month': [month], 'day': [day]})[0]
    
    percentage_change = 0.0
    new_predicted_total = row['Predicted_total']
    
    for index, event in event_configuration.iterrows():
        if pd.notna(event['start_date']) and pd.notna(event['end_date']):
            start_date = pd.to_datetime(event['start_date'])
            end_date = pd.to_datetime(event['end_date'])
            
            if start_date <= date <= end_date:
                event_ = event['event']
                print(f"Event found: {event_}")
                #process year and event and then put the processed in the model 
                percentage_change = model.predict(year,event_)
                if percentage_change>0:
                        new_predicted_total = min(float(row['Predicted_total']) * (1 + (percentage_change / 100)),row['capacity'])
                else:
                     new_predicted_total = max(float(row['Predicted_total']) * (1 + (percentage_change / 100)),0)
                break
    
    return  pd.Series([new_predicted_total, percentage_change])

for target in ['arrival','departure']:
    model=Model(target).load_model(f'{target}_model.pkl')
    df = pd.read_csv(f'data\\Serving\\{target}.csv')
    df[['new_predicted_total', 'percentage_change']] =df.apply(new_prediction,axis=1)
    df = df[['date_time_year','date_time_month','total','Predicted_total','percentage_change','new_predicted_total','capacity']]
    df.to_csv(f"data\\Serving\\{target}_after_prediction2.csv",index=False)


    print(model.predict(2026,'pre_hajj_season'))
