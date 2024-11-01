import pandas as pd
import numpy as np 
from Training.Preprocessingg import EventFeatureExtractor
import joblib 
from path_config.paths_config import PathConfig



def new_prediction(row,model,config):
    p = EventFeatureExtractor()
    percentage_change = 0.0
    new_predicted_total = row['Predicted_total']
    
    for index, event in config.iterrows():
        if pd.notna(event['start_date']) and pd.notna(event['end_date']):
            start_date = pd.to_datetime(event['start_date'])
            end_date = pd.to_datetime(event['end_date'])
            
            if start_date <= row['date'] <= end_date:
                event_ = event['event']
                print(f"Event found: {event_}")
                data = pd.DataFrame({'ds':[row['date']],'event':[event_]})
                data=p.extract(data) 
                percentage_change = model.predict(data)['yhat'][0]
                print(percentage_change)
                if percentage_change>0:
                        new_predicted_total = min(float(row['Predicted_total']) * (1 + (percentage_change / 100)),row['capacity'])
                else:
                     new_predicted_total = max(float(row['Predicted_total']) * (1 + (percentage_change / 100)),0)
                break
    
    return  pd.Series([new_predicted_total, percentage_change])
def main():
    conf = PathConfig()
    event_configuration = pd.read_csv(conf.path('training_data'))
    for target in ['arrival','departure']:
        model=joblib.load(conf.path(f'{target}_prophet_model'))
        df = pd.read_csv(conf.path(f'{target}s_old_predictions'))
        df['date'] = pd.to_datetime({'year': df['date_time_year'], 'month': df['date_time_month'], 'day':df['date_time_day_of_month']})
        df[['new_predicted_total', 'percentage_change']] =df.apply(new_prediction,axis=1,args=(model,event_configuration))
        df = df[['date_time_year','date_time_month','total','Predicted_total','percentage_change','new_predicted_total','capacity']]
        df.to_csv(conf.path(f'{target}s_new_predictions'),index=False)
if __name__=='__main__':
    conf = PathConfig()
    main()


