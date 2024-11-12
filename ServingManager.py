import pandas as pd 
import joblib
from Training.Preprocessingg import PreProcessor
from path_config.paths_config import PathConfig

def main():
    p = PreProcessor()
    df = pd.read_csv(conf.path('serving_data'))
    #df_=df.copy()
    df=df.sort_values(by='ds')
    data=p.preprocess(df)
    events = ["corona","ramadan_season","hajj_season","new_years_eve","eid_al_adha","christmas_season"]
    data_with_events = data[data['event'].apply(lambda event_list: bool(event_list) and any(event in event_list for event in events))]
    data_without_events = data[~(data['event'].apply(lambda event_list: bool(event_list) and any(event in event_list for event in events)))]
    data_with_events.reset_index(drop=True, inplace=True)
    data_without_events.reset_index(drop=True,inplace=True)
    for target in ['arrival','departure']:
        data_without_events[f'Predicted_{target}_changes']=0
        model = joblib.load(conf.path(f'{target}_prophet_model'))
        predictions = model.predict(data_with_events)['yhat']
        data_with_events[f'Predicted_{target}_changes']=predictions
    df_ = pd.concat([data_with_events,data_without_events])
    df_=df_.sort_values(by='ds')
    df_[['ds','event','Predicted_arrival_changes','Predicted_departure_changes']].to_csv(conf.path('predictions'),index=False)
    
if __name__=='__main__':
    conf = PathConfig()
    main()