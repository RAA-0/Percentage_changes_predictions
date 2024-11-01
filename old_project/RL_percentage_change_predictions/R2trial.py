from sklearn.metrics import r2_score
import pandas as pd 

dff=pd.read_csv('data\\Serving\\after_prediction.csv')

y_test = dff['total']
y_pred = dff[f'new_predicted_total']

r2 = r2_score(y_test, y_pred)
print("R2 Score:", r2)