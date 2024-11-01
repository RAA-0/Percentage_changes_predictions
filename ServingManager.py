import pandas as pd 
import joblib
from Training.Preprocessingg import EventFeatureExtractor
from path_config.paths_config import PathConfig

def main():
    p = EventFeatureExtractor()
    df = pd.read_csv(conf.path('serving_data'))
    df_=df.copy()
    data=p.extract(df)
    for target in ['arrival','departure']:
        model = joblib.load(conf.path(f'{target}_prophet_model'))
        predictions = model.predict(data)['yhat']
        df_[f'Predicted_{target}_changes']=predictions
    df_.to_csv(conf.path('predictions'),index=False)
    
if __name__=='__main__':
    conf = PathConfig()
    main()