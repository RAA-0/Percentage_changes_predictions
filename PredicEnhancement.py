import pandas as pd 
from Training.Preprocessingg import PreProcessor
from Training.EventExtraction import EventFeatureExtractor
from newtr2 import NewPredictor

def main():
    df=pd.read_csv('data\\testing_pred\\total_arrival_predictions.csv')
    df['ds'] = pd.to_datetime({'year': df['date_time_year'], 'month': df['date_time_month'], 'day':df['date_time_day_of_month']})
    df=df[['ds','total','Predicted_total','capacity']]
    p = PreProcessor()
    df = p.preprocess(df)
    df=pd.read_csv('data\\events_detected.csv')
    e = EventFeatureExtractor()
    df = e.transform(df)
    np = NewPredictor(df)
    np.start_new_prediction()

if __name__=='__main__':
    main()




    