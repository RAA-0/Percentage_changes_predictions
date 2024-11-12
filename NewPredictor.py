import pandas as pd 
import joblib
from sklearn.metrics import r2_score

class NewPredictor:
    def __init__(self,df):
        self.df = df
        self.df_with_events= pd.DataFrame()
        self.df_wihtout_events=pd.DataFrame()

    def start_new_prediction(self):
        print("starting new predictions.....")
        self.classify_data_with_events()
        self.predict_changes()
        self.new_prediction()


    def predict_changes(self):
        model=joblib.load("models\\prophet_arrival_model.joblib")
        self.df_with_events.sort_values(by='ds', inplace=True)
        self.df_with_events.reset_index(drop=True, inplace=True)
        predictions = model.predict(self.df_with_events)['yhat']
        self.df_with_events['predicted_change'] = predictions
        self.df_without_events['predicted_change']=0

    def new_prediction(self):
        df = (pd.concat([self.df_without_events,self.df_with_events])).sort_values(by='ds')
        df['new_prediction']=df['Predicted_total']*(1+df['predicted_change']/100)
        df[['ds','event','total','Predicted_total','predicted_change','new_prediction']].to_csv('data\\new_predictions.csv',index=False)
        print("old evaluation: ")
        self.evaluate(df['total'],df['Predicted_total'])
        print('new evaluation: ')
        self.evaluate(df['total'],df['new_prediction'])

    def classify_data_with_events(self):
        events = ["corona","ramadan_season","hajj_season","new_years_eve","eid_al_adha","christmas_season"]
        self.df['has_significant_event'] = self.df['event'].apply(lambda event_list: bool(event_list) and any(event in event_list for event in events))
        self.df_with_events = self.df[self.df['has_significant_event']].copy()
        self.df_without_events = self.df[~self.df['has_significant_event']].copy()
    
    def evaluate(self,y_test,y_pred):
        r2=r2_score(y_test,y_pred)
        print(f"r2_score: {r2}")

    